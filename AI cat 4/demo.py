import math
import random
from copy import deepcopy

import math
import random
from copy import deepcopy
from collections import deque
import heapq

class Para:
    def __init__(self, state, isBackcost = False, depth = 0):
        self.state = state
        self.N = len(state)
        self.cost = self.heuristics()
        self.depth = depth
        self.isBackward = isBackcost

    def __lt__(self, another):
        if not self.isBackward:
            return self.cost < another.cost 
        return self.cost + self.depth < another.cost + another.depth

    def isGoal(self):
        goal = sorted(deepcopy(self.state))

        return (self.state == goal)

    def heuristics(self):

        cost = 0
        for i in range(1,self.N):
            if self.state[i] != self.state[i-1]+1:
                cost+=1
        if self.state[0] != 1:
            cost += 1

        return cost 

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
            next_states[i] = State(state, self.isBackward, self.depth+1)

        return next_states

class Solver:

    def __init__(self):
        self.solution = None
        self.steps = 0

    def a_star(self,initial):
        frontier = []
        explored = set()
        visited = set()

        heapq.heappush(frontier,initial.state)
        visited.add(tuple(initial.state))

        while frontier:
            current = heapq.heappop(frontier)

            if tuple(current.state) in explored:
                continue
            
            explored.add(tuple(current.state))

            if current.isGoal():
                self.solution = current
                return self.solution, self.steps

            for next_state in current.nextStates():
                if tuple(next_state.state) not in visited:
                    heapq.heappush(frontier,next_state)
                    visited.add(tuple(next_state.state))
                    self.steps += 1

        return None

    def greedy_BFS(self, init_state):

        frontier = []
        explored = set()
        visited = set()

        heapq.heappush(frontier, init_state)
        visited.add(tuple(init_state.state))

        while frontier:
            board = heapq.heappop(frontier)

            if tuple(board.state) in explored:
                continue

            explored.add(tuple(board.state))

            if board.is_goal_state():
                self.solution = board
                self.nodes_found = len(visited)
                return self.solution

            for next_state in board.find_next_states():
                if tuple(next_state.state) not in visited:
                    visited.add(tuple(next_state.state))
                    heapq.heappush(frontier, next_state)
                    self.current_depth = max(self.current_depth, next_state.depth)

        
        return None

    def trace_path(self):

        this_state = self.solution
        path = [this_state]

        while this_state.parent != None:
            path.append(this_state.parent)
            this_state = this_state.parent

        self.no_of_moves = len(path) - 1

        return path[::-1]

    def print_report(self, algorithm):
       
        path = self.trace_path()

        print("---------------------------------------------------------------------------------------------------")
        print("\nNo. of States Visited\t:", self.nodes_found)
        print("\nDepth of {0}\t: {1}".format(algorithm, self.current_depth))
        print("\nNo. of Moves Taken\t:", self.no_of_moves)
        print("\nSolution Path:\n")
        

        for state in path:
            print("Move :", state.operation)
            print(state, "\n")
        
        print("---------------------------------------------------------------------------------------------------")
                


if __name__ == "__main__":

    solve = Solver()
    init_state = Para([5,4,3,2,1])
    solution = solve.a_star(init_state)
    solve.print_report("A* search")

'''
        print("\n\t\t\tInformed Search : A* Search\n")
        solver = Puzzle_Solver()
        init_state = Puzzle_State([7, 2, 4, 5, 0, 6, 8, 3, 1], backward_cost=True)
        solution = solver.a_star(init_state)
        solver.print_report("A* Search")
    
        print("\n\t\t\tInformed Search : Greedy Best-First Search\n")
        solver = Puzzle_Solver()
        init_state = Puzzle_State([7, 2, 4, 5, 0, 6, 8, 3, 1])
        solution = solver.greedy_BFS(init_state)
        solver.print_report("Greedy BFS")
'''