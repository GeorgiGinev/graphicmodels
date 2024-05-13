import numpy as np

def initialize_cluster(dimensions):
    # Създаване на клъстер с размер 2^dimensions
    return np.zeros((2**dimensions,))

def linear_search(arr, x):
    for i in range(len(arr)):
        if arr[i] == x:
            return i
    return -1

def distribute_tasks(cluster, tasks, queue_limit, clusterTasks):
    task_index = 0
    min_load_index = 0
    old_min_load_index = 0

    while task_index < len(tasks):
        min_load_index = np.argmin(cluster)

        if old_min_load_index > -1 : 
            min_load_index = old_min_load_index

        # Проверка дали следващата задача може да бъде добавена без да се наруши ограничението на опашката от
        # минимум 5 задачи на сървър
        if clusterTasks[min_load_index] < queue_limit:
            cluster[min_load_index] += tasks[task_index]
            clusterTasks[min_load_index] += 1

            task_index += 1
            #Нулиране на индекс в случай, че е била мигрирана задача
            old_min_load_index = -1
        else:
            # Ако няма достатъчно място, преминаваме към следващия сървър
            min_load_index = (min_load_index + 1) % len(cluster)
            # Запазваме старият индекс на сървъра
            old_min_load_index = min_load_index
            # При преместването на таска в следващия сървър времето се увеличава с 1 секунда
            tasks[task_index] += 1
            # Добавен е OR понеже има случаи, в които всички сървъри са заети и останалите таскове не могат да бъдат изпълнени
            if min_load_index == 0 or clusterTasks[min_load_index] >= queue_limit:
                # Проверява допълнително за свободен сървър и добавя задача към него с времето за преместване на сървъра
                found_free_server_index = linear_search(clusterTasks, 4)
                if(found_free_server_index > -1):
                    old_min_load_index = found_free_server_index
                    tasks[task_index] += found_free_server_index - 1
                else:
                    print("Warning: Всички задачи не могат да бъдат направени поради невъзможността на сървърите да ги поемат.")
                    print("Таскът, от който започва невъзможността : ", task_index)
                    break  # Излизаме от цикъла, ако всички сървъри са пълни

# Калкулиране на средно % отклонение на товара от средната стойност на изчислителния товар
def calculate_deviations(cluster):
    mean_load = np.mean(cluster)
    deviations = 100 * np.abs(cluster - mean_load) / mean_load
    average_deviation = np.mean(deviations)
    return average_deviation

# Параметри на задачата
dimensions = 6  # Изберете 4 или 6 за размерност на куба
n_tasks = 200  # Изберете 100 или 200 за брой задачи
queue_limit = 5
tasks = []
# Генериране на задачи
while len(tasks) < n_tasks:
    task = np.random.normal(7.5, 1.5)
    if 5 <= task <= 10:
        tasks.append(task)

print("Задачи : ", tasks)

# Инициализация и разпределение на задачите
cluster = initialize_cluster(dimensions)
clusterTasks = initialize_cluster(dimensions)
distribute_tasks(cluster, tasks, queue_limit, clusterTasks)

# Изчисление и отпечатване на отклоненията
average_deviation = calculate_deviations(cluster)
print("Натоварване на всеки сървър в секунди:", cluster)
print("Брой таскове на всеки сървър : ", clusterTasks)
print("Средно % отклонение на товара от средната стойност на изчислителния товар:", average_deviation)
