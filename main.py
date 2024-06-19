import threading
import time
import random
import matplotlib.pyplot as plt
import networkx as nx
from threading import Timer

from typing import List
from server import Server
from connection import Connection
from task import Task

threadInterval = 1
programRinningTimer = 0
numberOfTasks = 100
dim = 6
thread = None
colors = [
    'red',
    'green',
    'blue',
    'yellow',
    'purple',
    'orange'
]
areServersWorking = True

# Тук може да се добави логика на задачата
def createTask():
    print(f"Нишката започна изпълнението")

# Тук се създават задачите, които ще се обработват от къстерите. Те са с интерфейс
# time: number
# task: threadingTimer - създадена нишка с времето.
def createTasks(numOfTasks):
    avgTime = 7.5  # Средно време между 5 и 10 секунди
    standardDeviation = 1.5  # Примерно стандартно отклонение

    tasksNumber = numOfTasks

    tasks: List[Task] = []

    for _ in range(tasksNumber): 
        time = random.gauss(avgTime, standardDeviation)
        # Ограничаваме времето в интервала 5-10 секунди
        time = max(5, min(time, 10))
        tasks.append(Task(_, time))
    
    return tasks

#Създаваме x-измерен хиперкуб
def createCube(dimensions):
    num_nodes = 2 ** dimensions
    hypercube: List[Server] = [[] for _ in range(num_nodes)]
    for i in range(num_nodes):
        hypercube[i] = Server(i)
        hypercube[i].connection = []
        hypercube[i].tasks = []
    
    for i in range(num_nodes):
        for d in range(dimensions):
            # Генерира съседите.
            # Идеята е в битове единицата да се измества наляво от нулата с d пъти. Например ако d = 2 то = 00000100
            # А самият оператор ^ още познат като XOR сравнява битовете
            neighbour = i ^ (1 << d)
 
            linkedColor = colors[d]

            connectionNew = Connection(neighbour=hypercube[neighbour], linkedColor=linkedColor)
            
            hypercube[i].connection.append(connectionNew)
    
    return hypercube

# Показваме в конзолата как е свързан този x-измерен куб
def showHypercube(hypercube: List[Server], thread: Timer | None, stopServer: bool = False):
    if(thread != None):
        thread.cancel()

    completedTasks = 0
    global programRinningTimer
    programRinningTimer+=1

    #print('areServersWorking ', areServersWorking)

    for i, neighbour in enumerate(hypercube):
        if(stopServer):
            neighbour.turnOfServer()
            print(f'Сървър : {neighbour.id} се спира')
            print(f'Сървър : {neighbour}')
        else:
            completedTasks += len(neighbour.completedTasks)
            #print(f"Сървър : {neighbour}")

    if(not stopServer):
        thread = Timer(threadInterval, showHypercube, [hypercube, thread, completedTasks == numberOfTasks])
        thread.start()
    else:
        print(f'Програмата е работела {programRinningTimer} секунди')
        global areServersWorking 
        areServersWorking = not stopServer

def turnOnServers(hypercube: List[Server]):
    for index, server in enumerate(hypercube):
        print('server ', server)
        server.turnOnServer()

# Създаваме граф
def generateGraph(hypercube: List[Server]):
    hypercubeGraph = nx.Graph()
    for index, i in enumerate(hypercube):
        for d in i.connection:
            hypercubeGraph.add_edge(index, d.neighbour.id, color=d.linkedColor)
    
    return hypercubeGraph

# Визуализираме графът
def visualize(hypercubeGraph, dimensions):
    pos = nx.spring_layout(hypercubeGraph, dim=2)  # Позициониране в 2D пространство
    labels = {i: f"{i+1}" for i in hypercubeGraph.nodes()}
    
    edges = hypercubeGraph.edges(data=True)
    colors = [edge[2]['color'] for edge in edges]

    plt.figure(figsize=(8, 8))
    nx.draw(hypercubeGraph, pos, with_labels=True, labels=labels, node_size=700, node_color="skyblue", font_size=10, font_color="black", font_weight="bold", edge_color=colors)
    plt.title("4-мерен Хиперкуб (Тесеракт)")
    plt.show()

# Главните стъпки
tasks = createTasks(numberOfTasks)

hypercube = createCube(dim)
turnOnServers(hypercube)
Timer(threadInterval, showHypercube, [hypercube, thread]).start()
hypercube[0].addTasks(tasks)

dontShowGraph = True
while(dontShowGraph):
    if(not areServersWorking):
        avgTasksPerServer = numberOfTasks / len(hypercube)
        print(f'Изчисляване на средния товар в клъстера : {avgTasksPerServer}')
        
        avgPerServer = 0
        for index, server in enumerate(hypercube):
            avgPerServer += len(server.completedTasks) - avgTasksPerServer
            print(f'Средно % отклонение на сървър {server.id} : {len(server.completedTasks)/(avgTasksPerServer/100)}%')
            
        # print(f'Изчисляване на средното процентно отклонение : {avgPerServer / len(hypercube)}%') 

        graph = generateGraph(hypercube)
        visualize(graph, dim)
        dontShowGraph = False