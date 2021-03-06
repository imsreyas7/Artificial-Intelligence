

from collections import deque
import heapq


class Puzzle_State:
    """Container class to hold the current state of the Puzzle."""

    parent = None
    state = None
    operation = None
    zero = None
    depth = 0
    cost = 0
    backward_cost = False

    def __init__(self, state, parent = None, operation = None, depth = 0, backward_cost = False):
       

        self.parent = parent
        self.state = state
        self.operation = operation
        self.zero = self.find_zero()
        self.depth = depth
        self.backward_cost = backward_cost

        if backward_cost == True:       
            self.cost = self.depth + self.manhattan_distance()
        else:                           
            self.cost = self.manhattan_distance()


    def __str__(self):
        """String notation of the Puzzle_State object."""

        return  str(self.state[:3]) + "\n" \
            +   str(self.state[3:6]) + "\n" \
            +   str(self.state[6:]) + "\n"

    def __lt__(self, another_board):
        """To override the < operator for the class with the cost function f(n) of the puzzle configuration."""
        
        if self.cost == another_board.cost:
            return self.depth < another_board.depth
        return self.cost < another_board.cost

    
    def is_goal_state(self):
        """Checks if the goal state has been reached."""

        for i in range(0, len(self.state)):
            if i == self.state[i]:
                continue
            else:
                return False
        return True

    def find_zero(self):
        """Finds the index of 0 from the given state configuration."""

        for i in range(9):
            if self.state[i] == 0:
                return i
    
    def swap(self, i, j):
        """Swaps the ith element and jth element of the state configuration."""

        new_state = list(self.state)
        new_state[i], new_state[j] = new_state[j], new_state[i]
        return new_state

    def move_up(self):
        """Moves a block up, if there is a zero in the appropriate position. 
        Returns None if configuration is not possible."""

        if self.zero > 2:
            return Puzzle_State(self.swap(self.zero, self.zero-3), self, 'Up', self.depth+1, self.backward_cost)
        else:
            return None
    
    def move_down(self):
        """Moves a block down, if there is a zero in the appropriate position. 
        Returns None if configuration is not possible."""

        if self.zero < 6:
            return Puzzle_State(self.swap(self.zero, self.zero+3), self, 'Down', self.depth+1, self.backward_cost)
        else:
            return None
    
    def move_left(self):
        """Moves a block left, if there is a zero in the appropriate position. 
        Returns None if configuration is not possible."""

        if self.zero % 3 != 0:
            return Puzzle_State(self.swap(self.zero, self.zero-1), self, 'Left', self.depth+1, self.backward_cost)
        else:
            return None
    
    def move_right(self):
        """Moves a block right, if there is a zero in the appropriate position. 
        Returns None if configuration is not possible."""

        if (self.zero + 1) % 3 != 0:
            return Puzzle_State(self.swap(self.zero, self.zero+1), self, 'Right', self.depth+1, self.backward_cost)
        else:
            return None

    def find_next_states(self):
        """Finds the possible next state configurations based on the 4 available moves."""

        next_states = []
        next_states.append(self.move_up())
        next_states.append(self.move_down())
        next_states.append(self.move_left())
        next_states.append(self.move_right())

        next_states = list(filter(None, next_states))

        return next_states

    def manhattan_distance(self):
        """Calculates the Heuristic Function h(n) based on the Manhattan Distance 
        between a block and it's final state position."""

        heuristic = 0

        for i in range(len(self.state)):
            if self.state[i] == 0:      #do not include the blank tile as part of the Manhattan distance.
                continue
                        #absolute vertical distance + absolute horizontal distance from it's goal position
            heuristic += abs(self.state[i] // 3 - i // 3) + abs(self.state[i] % 3 - i % 3)

        return heuristic


class Puzzle_Solver:
    """Container class that implements the functions to solve the 8-Puzzle board and trace the path."""

    solution = None
    nodes_found = 0
    current_depth = 0
    no_of_moves = 0


    def BFS(self, init_state):
        """Performs an uninformed BFS algorithm on the given initial Puzzle configuration."""

        frontier = deque()
        visited = set()

        frontier.append(init_state)
        visited.add(tuple(init_state.state))

        while frontier:
            board = frontier.popleft()
            #visited.add(tuple(board.state))

            if board.is_goal_state():
                self.solution = board
                self.nodes_found = len(visited)
                return self.solution
            
            for next_state in board.find_next_states():
                if tuple(next_state.state) not in visited:
                    frontier.append(next_state)
                    visited.add(tuple(next_state.state))
                    self.current_depth = max(self.current_depth, next_state.depth)
            
        return None

    def a_star(self, init_state):
        """Performs an informed A* Search Algorithm on the given initial Puzzle configuration."""

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
                    heapq.heappush(frontier, next_state)
                    visited.add(tuple(next_state.state))
                    self.current_depth = max(self.current_depth, next_state.depth)
                
                elif tuple(next_state.state) not in explored:
                    heapq.heappush(frontier, next_state)
                    self.current_depth = max(self.current_depth, next_state.depth)
            
        return None

    def greedy_BFS(self, init_state):
        """Performs a Greedy Best-First Search Algorithm on the given initial Puzzle configuration."""

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

                elif tuple(next_state.state) not in explored:
                    heapq.heappush(frontier, next_state)
                    self.current_depth = max(self.current_depth, next_state.depth)
        
        return None

    def trace_path(self):
        """Traces the path taken by any search algorithm using the parent data member of the Puzzle object."""

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
        print("\nNo. of Moves Taken\t:", self.no_of_moves)
        print("\nSolution Path:\n")
        

        for state in path:
            print("Move :", state.operation)
            print(state, "\n")
        
        print("---------------------------------------------------------------------------------------------------")


if __name__ == "__main__":
    """Driver class to implement the 8-Puzzle Solver using different search algorithms."""
    
    
    print("\n\t\t\tUninformed Search : Breadth-First Search\n")
    solver = Puzzle_Solver()
    init_state = Puzzle_State([7, 2, 4, 5, 0, 6, 8, 3, 1])
    solution = solver.BFS(init_state)
    solver.print_report("BF Search")
    
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
OUTPUT

            Uninformed Search : Breadth-First Search

---------------------------------------------------------------------------------------------------

No. of Moves Taken  : 26

Solution Path:

Move : None
[7, 2, 4]
[5, 0, 6]
[8, 3, 1]
 

Move : Left
[7, 2, 4]
[0, 5, 6]
[8, 3, 1]
 

Move : Up
[0, 2, 4]
[7, 5, 6]
[8, 3, 1]
 

Move : Right
[2, 0, 4]
[7, 5, 6]
[8, 3, 1]
 

Move : Down
[2, 5, 4]
[7, 0, 6]
[8, 3, 1]
 

Move : Down
[2, 5, 4]
[7, 3, 6]
[8, 0, 1]
 

Move : Left
[2, 5, 4]
[7, 3, 6]
[0, 8, 1]
 

Move : Up
[2, 5, 4]
[0, 3, 6]
[7, 8, 1]
 

Move : Right
[2, 5, 4]
[3, 0, 6]
[7, 8, 1]
 

Move : Right
[2, 5, 4]
[3, 6, 0]
[7, 8, 1]
 

Move : Up
[2, 5, 0]
[3, 6, 4]
[7, 8, 1]
 

Move : Left
[2, 0, 5]
[3, 6, 4]
[7, 8, 1]
 

Move : Left
[0, 2, 5]
[3, 6, 4]
[7, 8, 1]
 

Move : Down
[3, 2, 5]
[0, 6, 4]
[7, 8, 1]
 

Move : Right
[3, 2, 5]
[6, 0, 4]
[7, 8, 1]
 

Move : Right
[3, 2, 5]
[6, 4, 0]
[7, 8, 1]
 

Move : Down
[3, 2, 5]
[6, 4, 1]
[7, 8, 0]
 

Move : Left
[3, 2, 5]
[6, 4, 1]
[7, 0, 8]
 

Move : Up
[3, 2, 5]
[6, 0, 1]
[7, 4, 8]
 

Move : Right
[3, 2, 5]
[6, 1, 0]
[7, 4, 8]
 

Move : Up
[3, 2, 0]
[6, 1, 5]
[7, 4, 8]
 

Move : Left
[3, 0, 2]
[6, 1, 5]
[7, 4, 8]
 

Move : Down
[3, 1, 2]
[6, 0, 5]
[7, 4, 8]
 

Move : Down
[3, 1, 2]
[6, 4, 5]
[7, 0, 8]
 

Move : Left
[3, 1, 2]
[6, 4, 5]
[0, 7, 8]
 

Move : Up
[3, 1, 2]
[0, 4, 5]
[6, 7, 8]
 

Move : Up
[0, 1, 2]
[3, 4, 5]
[6, 7, 8]

---------------------------------------------------------------------------------------------------

			Informed Search : A* Search

---------------------------------------------------------------------------------------------------

No. of Moves Taken	: 26

Solution Path:

Move : None
[7, 2, 4]
[5, 0, 6]
[8, 3, 1]
 

Move : Left
[7, 2, 4]
[0, 5, 6]
[8, 3, 1]
 

Move : Up
[0, 2, 4]
[7, 5, 6]
[8, 3, 1]
 

Move : Right
[2, 0, 4]
[7, 5, 6]
[8, 3, 1]
 

Move : Down
[2, 5, 4]
[7, 0, 6]
[8, 3, 1]
 

Move : Down
[2, 5, 4]
[7, 3, 6]
[8, 0, 1]
 

Move : Left
[2, 5, 4]
[7, 3, 6]
[0, 8, 1]
 

Move : Up
[2, 5, 4]
[0, 3, 6]
[7, 8, 1]
 

Move : Right
[2, 5, 4]
[3, 0, 6]
[7, 8, 1]
 

Move : Right
[2, 5, 4]
[3, 6, 0]
[7, 8, 1]
 

Move : Up
[2, 5, 0]
[3, 6, 4]
[7, 8, 1]
 

Move : Left
[2, 0, 5]
[3, 6, 4]
[7, 8, 1]
 

Move : Left
[0, 2, 5]
[3, 6, 4]
[7, 8, 1]
 

Move : Down
[3, 2, 5]
[0, 6, 4]
[7, 8, 1]
 

Move : Right
[3, 2, 5]
[6, 0, 4]
[7, 8, 1]
 

Move : Right
[3, 2, 5]
[6, 4, 0]
[7, 8, 1]
 

Move : Down
[3, 2, 5]
[6, 4, 1]
[7, 8, 0]
 

Move : Left
[3, 2, 5]
[6, 4, 1]
[7, 0, 8]
 

Move : Left
[3, 2, 5]
[6, 4, 1]
[0, 7, 8]
 

Move : Up
[3, 2, 5]
[0, 4, 1]
[6, 7, 8]
 

Move : Right
[3, 2, 5]
[4, 0, 1]
[6, 7, 8]
 

Move : Right
[3, 2, 5]
[4, 1, 0]
[6, 7, 8]
 

Move : Up
[3, 2, 0]
[4, 1, 5]
[6, 7, 8]
 

Move : Left
[3, 0, 2]
[4, 1, 5]
[6, 7, 8]
 

Move : Down
[3, 1, 2]
[4, 0, 5]
[6, 7, 8]
 

Move : Left
[3, 1, 2]
[0, 4, 5]
[6, 7, 8]
 

Move : Up
[0, 1, 2]
[3, 4, 5]
[6, 7, 8]
 

---------------------------------------------------------------------------------------------------

			Informed Search : Greedy Best-First Search

---------------------------------------------------------------------------------------------------

No. of Moves Taken	: 56

Solution Path:

Move : None
[7, 2, 4]
[5, 0, 6]
[8, 3, 1]
 

Move : Down
[7, 2, 4]
[5, 3, 6]
[8, 0, 1]
 

Move : Right
[7, 2, 4]
[5, 3, 6]
[8, 1, 0]
 

Move : Up
[7, 2, 4]
[5, 3, 0]
[8, 1, 6]
 

Move : Up
[7, 2, 0]
[5, 3, 4]
[8, 1, 6]
 

Move : Left
[7, 0, 2]
[5, 3, 4]
[8, 1, 6]
 

Move : Left
[0, 7, 2]
[5, 3, 4]
[8, 1, 6]
 

Move : Down
[5, 7, 2]
[0, 3, 4]
[8, 1, 6]
 

Move : Right
[5, 7, 2]
[3, 0, 4]
[8, 1, 6]
 

Move : Down
[5, 7, 2]
[3, 1, 4]
[8, 0, 6]
 

Move : Left
[5, 7, 2]
[3, 1, 4]
[0, 8, 6]
 

Move : Up
[5, 7, 2]
[0, 1, 4]
[3, 8, 6]
 

Move : Up
[0, 7, 2]
[5, 1, 4]
[3, 8, 6]
 

Move : Right
[7, 0, 2]
[5, 1, 4]
[3, 8, 6]
 

Move : Down
[7, 1, 2]
[5, 0, 4]
[3, 8, 6]
 

Move : Left
[7, 1, 2]
[0, 5, 4]
[3, 8, 6]
 

Move : Down
[7, 1, 2]
[3, 5, 4]
[0, 8, 6]
 

Move : Right
[7, 1, 2]
[3, 5, 4]
[8, 0, 6]
 

Move : Right
[7, 1, 2]
[3, 5, 4]
[8, 6, 0]
 

Move : Up
[7, 1, 2]
[3, 5, 0]
[8, 6, 4]
 

Move : Left
[7, 1, 2]
[3, 0, 5]
[8, 6, 4]
 

Move : Down
[7, 1, 2]
[3, 6, 5]
[8, 0, 4]
 

Move : Left
[7, 1, 2]
[3, 6, 5]
[0, 8, 4]
 

Move : Up
[7, 1, 2]
[0, 6, 5]
[3, 8, 4]
 

Move : Right
[7, 1, 2]
[6, 0, 5]
[3, 8, 4]
 

Move : Right
[7, 1, 2]
[6, 5, 0]
[3, 8, 4]
 

Move : Down
[7, 1, 2]
[6, 5, 4]
[3, 8, 0]
 

Move : Left
[7, 1, 2]
[6, 5, 4]
[3, 0, 8]
 

Move : Left
[7, 1, 2]
[6, 5, 4]
[0, 3, 8]
 

Move : Up
[7, 1, 2]
[0, 5, 4]
[6, 3, 8]
 

Move : Up
[0, 1, 2]
[7, 5, 4]
[6, 3, 8]
 

Move : Right
[1, 0, 2]
[7, 5, 4]
[6, 3, 8]
 

Move : Down
[1, 5, 2]
[7, 0, 4]
[6, 3, 8]
 

Move : Down
[1, 5, 2]
[7, 3, 4]
[6, 0, 8]
 

Move : Left
[1, 5, 2]
[7, 3, 4]
[0, 6, 8]
 

Move : Up
[1, 5, 2]
[0, 3, 4]
[7, 6, 8]
 

Move : Right
[1, 5, 2]
[3, 0, 4]
[7, 6, 8]
 

Move : Up
[1, 0, 2]
[3, 5, 4]
[7, 6, 8]
 

Move : Left
[0, 1, 2]
[3, 5, 4]
[7, 6, 8]
 

Move : Down
[3, 1, 2]
[0, 5, 4]
[7, 6, 8]
 

Move : Right
[3, 1, 2]
[5, 0, 4]
[7, 6, 8]
 

Move : Down
[3, 1, 2]
[5, 6, 4]
[7, 0, 8]
 

Move : Left
[3, 1, 2]
[5, 6, 4]
[0, 7, 8]
 

Move : Up
[3, 1, 2]
[0, 6, 4]
[5, 7, 8]
 

Move : Right
[3, 1, 2]
[6, 0, 4]
[5, 7, 8]
 

Move : Right
[3, 1, 2]
[6, 4, 0]
[5, 7, 8]
 

Move : Down
[3, 1, 2]
[6, 4, 8]
[5, 7, 0]
 

Move : Left
[3, 1, 2]
[6, 4, 8]
[5, 0, 7]
 

Move : Left
[3, 1, 2]
[6, 4, 8]
[0, 5, 7]
 

Move : Up
[3, 1, 2]
[0, 4, 8]
[6, 5, 7]
 

Move : Right
[3, 1, 2]
[4, 0, 8]
[6, 5, 7]
 

Move : Down
[3, 1, 2]
[4, 5, 8]
[6, 0, 7]
 

Move : Right
[3, 1, 2]
[4, 5, 8]
[6, 7, 0]
 

Move : Up
[3, 1, 2]
[4, 5, 0]
[6, 7, 8]
 

Move : Left
[3, 1, 2]
[4, 0, 5]
[6, 7, 8]
 

Move : Left
[3, 1, 2]
[0, 4, 5]
[6, 7, 8]
 

Move : Up
[0, 1, 2]
[3, 4, 5]
[6, 7, 8]
 

---------------------------------------------------------------------------------------------------
'''
