from threading import Timer, Event, Thread
from time import sleep
from connection import Connection
from task import Task
from typing import List

import numpy as np

class Server:
    def __init__(self, id, connection: List[Connection] = [], tasks: List[Task] = []):
        self.id = id
        self.connection = connection
        self.tasks = tasks

        self.interval = 0.1
        self.thread: Thread | None = None
        self.workerThread: Thread | None = None

        self.isServerOn = False
        self.canReceiveTasks = True
        
        self.currentTask: Task
        self.completedTasks: List[Task] = []
        # self.runTaskCheckerThreadCompleted = Event()
        # self.turnOnSever()

    def completeTask(self):
        while self.isServerOn:
            if(len(self.tasks) > 0):
                self.currentTask = self.tasks.pop()
                print('Server ', self.id, ' Start working on ', self.currentTask.id)
                sleep(self.currentTask.time)
                print('Server ', self.id, ' Completed! ', self.currentTask.id)
                self.completedTasks.append(self.currentTask)
                self.currentTask = None

    def sortLoad(self):
        while(self.isServerOn):
            #print('server is on : ', self.id)
            for index, connection in enumerate(self.connection):
                server: Server = connection.neighbour
                #print('len(self.tasks) id : ', self.id)
                #print('len(self.tasks) : ', len(self.tasks))
                if(len(self.tasks) > len(server.tasks)):
                    splitTasks = self.tasks

                    sendTasks = []

                    leftTasks = []

                    if(len(splitTasks) > 10):
                        lastFifthIndex = len(splitTasks) - 5
                    else:
                        lastFifthIndex = len(splitTasks) // 2

                    sendTasks = splitTasks[lastFifthIndex:]
                    leftTasks = splitTasks[:lastFifthIndex]
                    self.tasks = leftTasks
                    #print('firstHalf : ', firstHalf)
                    #print('secondHalf : ', secondHalf)
                    server.addTasks(sendTasks)
                else: 
                    break

    def runTaskCheckerThread(self):
        # Стартира нова нишка за изпълнение на разпределянето на задачи.
        self.thread = Thread(target=self.sortLoad)
        self.thread.start()

    def addTasks(self, tasks: List[Task]):
        #print('add Tasks id : ', self.id)
        #print('add Tasks : ', tasks)
        for x in tasks:
            try:
                self.tasks.append(x)
            except (Exception, ValueError) as e:
                print(f"An exception occurred: {e, self.tasks}")
    
    def runTaskWorker(self):
        # Стартира нова нишка за изпълнение на разпределянето на задачи.
        self.workerThread = Thread(target=self.completeTask)
        self.workerThread.start()

    def turnOnServer(self):
        self.isServerOn = True
        self.runTaskCheckerThread()
        self.runTaskWorker()

    def turnOfServer(self):
        self.isServerOn = False

    def __repr__(self):
        return f"id={self.id}, completedTasks={len(self.completedTasks)} \n"

    def __str__(self):
        return f"id={self.id}, completedTasks={len(self.completedTasks)} \n"