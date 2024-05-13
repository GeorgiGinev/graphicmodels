import numpy as np
import matplotlib.pyplot as plt

# Подготовка на данни
def initialize_cluster(dimensions):
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

        if old_min_load_index > -1: 
            min_load_index = old_min_load_index

        if clusterTasks[min_load_index] < queue_limit:
            cluster[min_load_index] += tasks[task_index]
            clusterTasks[min_load_index] += 1
            task_index += 1
            old_min_load_index = -1
        else:
            min_load_index = (min_load_index + 1) % len(cluster)
            old_min_load_index = min_load_index
            tasks[task_index] += 1
            if min_load_index == 0 or clusterTasks[min_load_index] >= queue_limit:
                found_free_server_index = linear_search(clusterTasks, 4)
                if(found_free_server_index > -1):
                    old_min_load_index = found_free_server_index
                    tasks[task_index] += found_free_server_index - 1
                else:
                    print("Warning: Всички задачи не могат да бъдат направени.")
                    print("Таскът, от който започва невъзможността : ", task_index)
                    break

def calculate_deviations(cluster):
    mean_load = np.mean(cluster)
    deviations = 100 * np.abs(cluster - mean_load) / mean_load
    return np.mean(deviations)

# Параметри на задачата
dimensions = 6
n_tasks = 200
queue_limit = 5
tasks = [np.random.normal(7.5, 1.5) for _ in range(n_tasks) if 5 <= np.random.normal(7.5, 1.5) <= 10]

# Инициализация и разпределение на задачите
cluster = initialize_cluster(dimensions)
clusterTasks = initialize_cluster(dimensions)
distribute_tasks(cluster, tasks, queue_limit, clusterTasks)

# Изчисление на отклоненията
average_deviation = calculate_deviations(cluster)

# Графики
n_servers = 2**dimensions
plt.figure(figsize=(14, 6))
plt.subplot(1, 2, 1)
plt.bar(range(n_servers), cluster, color='blue')
plt.title('Натоварване на всеки сървър в секунди')
plt.xlabel('Индекс на сървър')
plt.ylabel('Натоварване в секунди')

plt.subplot(1, 2, 2)
plt.bar(range(n_servers), clusterTasks, color='green')
plt.title('Брой таскове на всеки сървър')
plt.xlabel('Индекс на сървър')
plt.ylabel('Брой задачи')

plt.tight_layout()
plt.show()

print("Средно % отклонение на товара от средната стойност на изчислителния товар:", average_deviation)
