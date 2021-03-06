import random
import time
from copy import deepcopy

class state:
    def __init__(self, config):
        self.config = config

    def configtoarray(self):
        arr = [[0 for j in range(len(self.config))] for i in range(len(self.config))]
        for i, j in enumerate(self.config):
            arr[i][j] = 1
        return arr

    def checkcols(self, arr, i, j):
        cost = 0
        for p in range(len(arr[0])):
            if p == i:
                continue
            cost += arr[p][j]
        return cost

    def checkud(self, arr, i, j):
        cost = 0
        l = len(arr[0])
        m , n = i-1, j-1
        while m >= 0 and n >= 0:
            cost += arr[m][n]
            m -= 1
            n -= 1
        m, n = i+1, j+1
        while m < l and n < l:
            cost += arr[m][n]
            m += 1
            n += 1
        return cost

    def checkld(self, arr, i, j):
        cost = 0
        l = len(arr[0])
        m , n = i-1, j+1
        while m >= 0 and n < l:
            cost += arr[m][n]
            m -= 1
            n += 1
        m, n = i+1, j-1
        while m < l and n >= 0:
            cost += arr[m][n]
            m += 1
            n -= 1
        return cost

    def fitness(self):
        arr = self.configtoarray()
        cost = 0
        for i, j in enumerate(self.config):
            col = self.checkcols(arr, i, j)
            ud = self.checkud(arr, i, j)
            ld = self.checkld(arr, i, j)
            cost += col + ud + ld
        cost //= 2
        return -cost


def crossover(s1, s2):
	#crossover between columns of the 2 selected ones from the heap
    ran = random.randrange(0, 8)
    newconfig = []
    for i in range(9):
        if i < ran:
            newconfig.append(s1.config[i])
        else:
            newconfig.append(s2.config[i])
    return state(newconfig)

def mutation(s, rate):
	#random mutation to add to the solution set
    if random.random() <= rate:
        s.config[random.randrange(0, 8)] = random.randrange(0, 8)
    return s

def randconfig():
    config = [random.randint(0,8) for i in range(9)]
    return config

def crossandmutate(s1, s2, rate = 0.7):
	#crossover of the first 2 states followe dby random mutation of the state generated
    child = crossover(s1, s2)
    child = mutation(child, rate)
    return child


def genetic():
    current_gen = []
    for i in range(10):
        current_gen.append(state(randconfig()))
    
    next_gen = []
    while True:
        found = False
        for i in current_gen:
                if i.fitness() == 0:
                    print("Sol found: ", i.config)
                    found = True
                    break
        
        if found == True:
            break
        
        current_gen.sort(key = lambda x: x.fitness(), reverse = True)
        next_gen = current_gen[:5]
        for i in range(5):
            next_gen.append(crossandmutate(current_gen[i], current_gen[i + 1]))
        next_gen.append(state(randconfig()))
        current_gen = deepcopy(next_gen)

genetic()

'''
(base) C:\Users\sreyas\Desktop\AILab>python 162_8q_gen.py
Sol found:  [6, 1, 5, 2, 0, 7, 4, 8, 3]
'''