import threading
import time
import random
import matplotlib.pyplot as plt
import networkx as nx


colors = [
    'red',
    'green',
    'blue',
    'yellow',
    'purple',
    'orange'
]

# Тук може да се добави логика на задачата
def createTask():
    print(f"Нишката започна изпълнението")

# Тук се създават задачите, които ще се обработват от къстерите. Те са с интерфейс
# time: number
# task: threadingTimer - създадена нишка с времето.
def createTasks():
    avgTime = 7.5  # Средно време между 5 и 10 секунди
    standardDeviation = 1.5  # Примерно стандартно отклонение

    tasksNumber = 100

    tasks = []

    for _ in range(tasksNumber): 
        time = random.gauss(avgTime, standardDeviation)
        # Ограничаваме времето в интервала 5-10 секунди
        time = max(5, min(time, 10))
        task = threading.Timer(time, createTask)
        tasks.append([time, task])
    
    return tasks

def createCube(dimensions):
    num_nodes = 2 ** dimensions
    hypercube = [[] for _ in range(num_nodes)]

    for i in range(num_nodes):
        for d in range(dimensions):
            # Генерира съседите.
            # Идеята е в битове единицата да се измества наляво от нулата с d пъти. Например ако d = 2 то = 00000100
            # А самият оператор ^ още познат като XOR сравнява битовете
            neighbour = i ^ (1 << d)
 
            linkedColor = colors[d]
            
            hypercube[i].append([
                neighbour+1,
                linkedColor
            ])
    
    return hypercube

def showHypercube(hypercube):
    for i, neighbour in enumerate(hypercube):
        print(f"Сървър {i+1} е свързан със: {neighbour}")

def generateGraph(hypercube):
    print('hr ', len(hypercube))
    hypercubeGraph = nx.Graph()
    for index, i in enumerate(hypercube):
        for d in i:
            hypercubeGraph.add_edge(index, d[0]-1, color=d[1])
    
    return hypercubeGraph

def visualize(hypercubeGraph, dimensions):
    pos = nx.spring_layout(hypercubeGraph, dim=2)  # Позициониране в 2D пространство
    labels = {i: f"{i+1}" for i in hypercubeGraph.nodes()}
    
    edges = hypercubeGraph.edges(data=True)
    colors = [edge[2]['color'] for edge in edges]

    plt.figure(figsize=(8, 8))
    nx.draw(hypercubeGraph, pos, with_labels=True, labels=labels, node_size=700, node_color="skyblue", font_size=10, font_color="black", font_weight="bold", edge_color=colors)
    plt.title("4-мерен Хиперкуб (Тесеракт)")
    plt.show()
    
tasks = createTasks()

dim = 6

hypercube = createCube(dim)
showHypercube(hypercube)
graph = generateGraph(hypercube)
visualize(graph, dim)
