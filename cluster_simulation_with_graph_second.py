import numpy as np
import networkx as nx
import matplotlib.pyplot as plt
import random
from collections import deque

global_current_task_index = 0

def initialize_graph(dimensions):
    G = nx.Graph()
    num_servers = 2**dimensions
    for i in range(num_servers):
        G.add_node(i, load=0, tasks=0, color=None, task_list=[], neighbors=[])  # добавяме цвят на върховете
    # Добавяне на ребра
    for i in range(num_servers):
        neighbors = []
        for j in range(1, random.randint(2, 4)):  # Свързваме всяка точка с 1 до 3 други точки
            target = (i + j) % num_servers
            G.add_edge(i, target)
            neighbors.append(target)
        # Актуализиране на атрибута neighbors след добавяне на всички ребра за даден върх
        G.nodes[i]['neighbors'] = neighbors
    return G

def distribute_tasks(G, start_server_id, tasks, queue_limit):
    # Опашка за BFS - "Breadth-First Search" (Търсене в широчина)
    queue = deque([start_server_id])
    # Множество за следене на посетените сървъри
    visited = set([start_server_id])
    # Индекс на текущата задача за разпределение
    task_index = 0

    # Обхождане докато има сървъри в опашката и задачи за разпределение
    while queue and task_index < len(tasks):
        current_server = queue.popleft()
        # Получаване на данни за текущия сървър
        server_data = G.nodes[current_server]

        # Разпределяне на задачите на текущия сървър, докато не се достигне лимита
        while task_index < len(tasks) and server_data['tasks'] < queue_limit:
            server_data['load'] += tasks[task_index]
            server_data['task_list'].append(tasks[task_index])
            server_data['tasks'] += 1
            task_index += 1

        # Добавяне на съседите на текущия сървър в опашката, ако не са били посетени
        for neighbor in G.neighbors(current_server):
            if neighbor not in visited:
                queue.append(neighbor)
                visited.add(neighbor)

    # Съобщение, ако има останали неразпределени задачи
    if task_index < len(tasks):
        print("Warning: Някои задачи не могат да бъдат разпределени поради достигане на лимитите на всички сървъри.")

def calculate_deviations(G):
    loads = [data['load'] for node, data in G.nodes(data=True)]
    mean_load = np.mean(loads)
    deviations = [100 * abs(load - mean_load) / mean_load if mean_load > 0 else 0 for load in loads]
    return np.mean(deviations), deviations

def visualize_graph(G):
    colors = [data['color'] for node, data in G.nodes(data=True)]
    pos = nx.circular_layout(G)  # Използваме кръгова подредба за по-добра визуализация
    nx.draw(G, pos, with_labels=True, node_color=colors, edge_color='gray')
    plt.show()

def print_tasks_per_server(G):
    for node, data in G.nodes(data=True):
        print(f"Сървър {node} има следните задачи: {data['task_list']}")

def gauss_generate_tasts(n_tasks, avg, between):
    # Генериране на данни
    samples = []
    while len(samples) < n_tasks:
        sample = np.random.normal(avg, between)
        if 5 <= sample <= 10:
            samples.append(sample)
    return samples

# Инициализация на графа
dimensions = 6  # за пример, използваме по-малък размер за лесно визуализиране
G = initialize_graph(dimensions)

# Оцветяване на върховете
colors = ['red', 'green', 'blue', 'yellow'] * (2**(dimensions-2))
for node, color in zip(G.nodes(), colors):
    G.nodes[node]['color'] = color

# Разпределение на задачите
n_tasks = 200
queue_limit = 5
tasks = gauss_generate_tasts(n_tasks, 7.5, 1.5)
print('Задачи : ' , tasks)
# Определяне на стартовия сървър
start_server_id = 0  # Примерен стартов сървър

# Разпределение на задачите
distribute_tasks(G, start_server_id, tasks, queue_limit)

# Изчисление на отклоненията
average_deviation, deviations = calculate_deviations(G)
print(f"Средно процентно отклонение: {average_deviation}%")
for idx, dev in enumerate(deviations):
    print(f"Сървър {idx} - Отклонение: {dev}%")

# Отпечатване на задачите за всеки сървър
print_tasks_per_server(G)

# Визуализация на графа
visualize_graph(G)