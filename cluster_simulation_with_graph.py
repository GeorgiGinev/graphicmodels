import numpy as np
import networkx as nx
import matplotlib.pyplot as plt
import random

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

def distribute_tasks(G, tasks, queue_limit):
    nodes = list(G.nodes(data=True))
    task_index = 0
    print('nodes : ', nodes);
    while task_index < len(tasks):
        # nodes.sort(key=lambda x: (x[1]['tasks'], x[1]['load']))  # сортиране по брой задачи и натоварване

        for node, data in nodes:
            if data['tasks'] < queue_limit:
                data['load'] += tasks[task_index]
                data['task_list'].append(tasks[task_index])  # добавяне на задачата към списъка
                data['tasks'] += 1
                task_index += 1
                break
        else:
            print("Warning: Всички задачи не могат да бъдат направени.")
            break

def calculate_deviations(G):
    loads = [data['load'] for node, data in G.nodes(data=True)]
    mean_load = np.mean(loads)
    deviations = [100 * abs(load - mean_load) / mean_load if mean_load > 0 else 0 for load in loads]
    return np.mean(deviations), deviations

def distribute_tasts_recurse(current_node, tasks, queue_limit, nodes):
    global global_current_task_index
    
    if global_current_task_index >= len(tasks):
        return

    nodes = list(G.nodes(data=True))

    if current_node['tasks'] < queue_limit:
        current_node['load'] += tasks[global_current_task_index]
        current_node['task_list'].append(tasks[global_current_task_index])  # добавяне на задачата към списъка
        current_node['tasks'] += 1
        global_current_task_index += 1
    else:
        tasks[global_current_task_index] += 1

    current_neighbor_index = 0
    while current_neighbor_index < len(current_node['task_list']):
        return distribute_tasts_recurse(nodes[current_node['neighbors'][current_neighbor_index]][1], tasks, queue_limit, nodes)

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
dimensions = 3  # за пример, използваме по-малък размер за лесно визуализиране
G = initialize_graph(dimensions)

# Оцветяване на върховете
colors = ['red', 'green', 'blue', 'yellow'] * (2**(dimensions-2))
for node, color in zip(G.nodes(), colors):
    G.nodes[node]['color'] = color

# Разпределение на задачите
n_tasks = 23
queue_limit = 5
tasks = gauss_generate_tasts(n_tasks, 7.5, 1.5)
print('tasts' , tasks)
distribute_tasts_recurse(list(G.nodes(data=True))[0][1], tasks, queue_limit, G)

# Изчисление на отклоненията
average_deviation, deviations = calculate_deviations(G)
print(f"Средно процентно отклонение: {average_deviation}%")
for idx, dev in enumerate(deviations):
    print(f"Сървър {idx} - Отклонение: {dev}%")

# Отпечатване на задачите за всеки сървър
print_tasks_per_server(G)

# Визуализация на графа
visualize_graph(G)