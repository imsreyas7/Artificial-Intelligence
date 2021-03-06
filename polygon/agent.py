from env import *
import heapdict
from copy import deepcopy

class agent:
    def __init__(self, env, start, goal):
        self.env = env
        self.start = start
        self.goal = goal
        self.path = []
    
    def heuristic(self, state):
        return state.dist(self.goal)
    
    def isGoal(self, state):
        if state == self.goal:
            return True
        return False
    
    def printPath(self, s, depth):
        lst = []
        while depth > 0:
            lst.append((s.x, s.y))
            s = s.parent
            depth -= 1
        lst.reverse()
        for i in range(len(lst)):
            print(lst[i])

    def astar(self):
        dis = set()
        q = heapdict.heapdict()
        self.start.g = 0
        depth = 0
        q[(self.start)] = self.heuristic(self.start) + self.start.g
        while len(q) != 0:
            u, _ = q.popitem()
            nextstates = env.getActions(u)
            if self.isGoal(u):
                self.printPath(u, depth)
                return
            if u not in dis:
                dis.add(u)
                for i in nextstates:
                    i.parent = u
                    i.g = depth
                    q[i] = self.heuristic(i) + i.g
            depth+=1

p = polygon([point(1,1), point(3,1), point(3,3), point(1,3)])
q = polygon([point(4,4), point(6,4), point(6,6), point(4,6)])
env = grid(100, 100, [p,q], point(0,0), point(6,6))
a = agent(env, point(0,0), point(6, 6))
a.astar()

'''
OUTPUT

runfile('C:/Users/sreyas/Desktop/AILab/polygon/agent.py', wdir='C:/Users/sreya/Desktop/AILab/polygon')
(1, 3)
(4, 6)
(6, 6)

'''