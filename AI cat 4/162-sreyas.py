# Name : Sreyas V
# Register no. : 185001162
# UCS 1504 - Artificial Intelligence - CAT 4 
# 07/11/2020 - Saturday 

import math
import time
import random
from copy import deepcopy
import heapq

class State:
    def __init__(self, state, isBackcost = False, depth = 0, parent = None):
        self.state = state
        self.N = len(state)
        self.cost = self.heuristicFn()
        self.depth = depth
        self.isBackward = isBackcost
        self.parent = parent
    
    def __str__(self):
        return str(self.state)
    
    def __lt__(self, another):
        if not self.isBackward:
            return self.cost < another.cost 
        return self.cost + self.depth < another.cost + another.depth
    
    def isGoal(self):
        goal = sorted(deepcopy(self.state))
        
        return (self.state == goal)  
    
    def nextStates(self):
        
        next_states =[]
        
        for l in range(self.N):
            for r in range(l+1,self.N+1):
                cut_list = self.state[l:r]
                rem_list = deepcopy(self.state)
                
                
                for indx in range(r-1,l-1,-1):
                    rem_list.pop(indx)
                
                for i in range(len(rem_list)+1):
                    new_list = rem_list[:i] + cut_list + rem_list[i:]
                    
                    if new_list != self.state and new_list not in next_states:
                        next_states.append(new_list)
        
        for i,state in enumerate(next_states):
            next_states[i] = State(state, isBackcost = self.isBackward, depth = self.depth+1, parent = self)
            
        random.shuffle(next_states)
        return next_states
    
    def heuristicFn(self):
        
        cost = 0
        
        for i in range(1,self.N):
            if self.state[i] != self.state[i-1]+1:
                cost+=1
        if self.state[0] != 1:
            cost += 1
            
        return cost 
    

class Solver:
    
    def setPath(self, goal):
        path = []
        start = goal
        
        while start:
            path.append(start)
            start = start.parent
        
        return path[::-1]
    
    def Best_First_Seach(self, state, verbose = False):
        
        frontier = []
        heapq.heappush(frontier, state)
        explored = set()
        
        if verbose:
            print('The order of explored states are : ')
        
        while frontier:
            
            cur_state = heapq.heappop(frontier)
            
            if tuple(cur_state.state) in explored:
                continue
            
            if verbose:
                print('\t->', cur_state)
            
            explored.add(tuple(cur_state.state))
            
            if cur_state.isGoal():
                return cur_state, self.setPath(goal=cur_state)
            
            for next_state in cur_state.nextStates():
                if tuple(next_state.state) not in explored:
                    heapq.heappush(frontier, next_state)
        return None, None
    
    def A_star_Seach(self, state, verbose = False):
        
        frontier = []
        heapq.heappush(frontier, state)
        explored = set()
        
        if verbose:
            print('The order of explored states are : ')
        
        while frontier:
            
            cur_state = heapq.heappop(frontier)
            
            if tuple(cur_state.state) in explored:
                continue
            
            if verbose:
                print('\t->', cur_state)
            
            explored.add(tuple(cur_state.state))
            
            if cur_state.isGoal():
                return cur_state, self.setPath(goal=cur_state)
            
            for next_state in cur_state.nextStates():
                if tuple(next_state.state) not in explored:
                    heapq.heappush(frontier, next_state)
        return None, None
            
                    

if __name__ == "__main__":
    print('\n\t\tN - Paragraph Problem\n')
    print('\n------------------------------------------------\n')
    
    print("\n\t\t Best First Search \n")
    initial_state = State([3,4,5,1,2])
    
    solver = Solver()
    start = time.time()
    goal, path = solver.Best_First_Seach(state = initial_state, verbose=True)
    end = time.time()

    if goal:
        print("\nNumber of steps taken : ")
        print(goal.cost + goal.depth)
        print("\nEvaluation Time\t\t: {0}s".format((end - start)))
        
    print('\n------------------------------------------------\n')

    print("\n\t\t A* Search \n")
    initial_state = State([3,4,5,1,2], isBackcost= True)
    
    solver = Solver()
    start = time.time()
    goal, path = solver.A_star_Seach(state = initial_state, verbose=True)
    end = time.time()

    if goal:
        print("\nNumber of steps taken : ")
        print(goal.cost + goal.depth)
        print("Evaluation Time\t\t: {0}s".format((end - start)))
    
    print('\n------------------------------------------------\n')

# Inference :
# A Star takes more time than BFS
# The difference is negligible as the state space is small 


#OUTPUT 1
#                N - Paragraph Problem
#
#
#------------------------------------------------
#
#
#                 Best First Search
#
#The order of explored states are :
#        -> [2, 4, 1, 5, 3, 6]
#        -> [1, 2, 4, 5, 3, 6]
#        -> [1, 2, 3, 4, 5, 6]
#
#Number of steps taken :
#2
#
#Evaluation Time         : 0.01s
#
#------------------------------------------------
#
#
#                 A* Search
#
#The order of explored states are :
#        -> [2, 4, 1, 5, 3, 6]
#        -> [1, 2, 4, 5, 3, 6]
#        -> [1, 2, 3, 4, 5, 6]
#
#Number of steps taken :
#2
#Evaluation Time         : 0.02s
#
#------------------------------------------------
#
#OUTPUT 2
#
#(base) C:\Users\sreyas\Desktop> cd c:\Users\sreyas\Desktop && cmd /C "C:\Users\sreyas\Anaconda3\python.exe c:\Users\sreyas\.vscode\extensions\ms-python.python-2020.10.332292344\pythonFiles\lib\python\debugpy\launcher 52781 -- c:\Users\sreyas\Desktop\162-sreyas.py "
#
#                N - Paragraph Problem
#
#
#------------------------------------------------
#
#
#                 Best First Search
#
#The order of explored states are :
#        -> [3, 4, 5, 1, 2]
#        -> [1, 2, 3, 4, 5]
#
#Number of steps taken :
#1
#
#Evaluation Time         : 0.0029926300048828125s
#
#------------------------------------------------
#
#
#                 A* Search
#
#The order of explored states are :
#        -> [3, 4, 5, 1, 2]
#        -> [1, 2, 3, 4, 5]
#
#Number of steps taken :
#1
#Evaluation Time         : 0.003991842269897461s
#
#------------------------------------------------
#
#
#(base) C:\Users\sreyas\Desktop>



        