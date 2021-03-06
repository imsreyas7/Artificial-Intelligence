import random 
import math
import heapq

class Board_State:
    state = None
    fitness = math.inf
    size = 0;
    
    def __init__(self,state):
        
        self.state = state
        self.size = len(state)
        self.fitness = self.fitness_fn() # objective function
        
    def __str__(self): 
        
        string = "\n"
        
        for i in range(self.size):
            temp = "- " * (self.state[i]-1) + "👑 " + "- " * (self.size - self.state[i] ) + "\n"
            string += '\t' + temp
        
        return string
    
    def __lt__(self,another_board):
        
        return self.fitness <= another_board.fitness
    
    def fitness_fn(self): #
        
        conflict = 0
        
        for i in range(self.size):
            for j in range(i+1,self.size):
                
                #check for same row
                if(self.state[i] == self.state[j]):
                    conflict+=1
                
                #check for left diagnol
                elif(self.state[i]+i == self.state[j]+j):
                    conflict+=1
                
                #check for right diagnol
                elif(self.state[i]-i == self.state[j]-j):
                    conflict+=1
        
        return conflict

class Genetic_Solver:
    
    Converging_cnt  = 0
    Converged_board = None
    
    def __init__(self):
        
        Converging_cnt  = 0
        Converged_board = None
     
    
    def select(self,board_population, best_count):
        return board_population[:best_count]

    def mutate(self,board):  
        
        randInd = random.randint(0,board.size-1)
        randPos = random.randint(1,board.size)
        
        new_board = list(board.state)
        new_board[randInd] = randPos
        
        return Board_State(new_board)

    def crossover(self,board_population, itr):
        
        slicer  = random.randint(1,board_population[0].size-1)
        A = board_population[itr*2].state[:slicer]
        B = board_population[itr*2].state[slicer:]
        C = board_population[itr*2+1].state[:slicer]
        D = board_population[itr*2+1].state[slicer:]
        
        A += D
        C += B
        
        crossover_children = []
        crossover_children.append(Board_State(A))
        crossover_children.append(Board_State(C))
        
        return crossover_children   

    def GeneticConvergence(self,board_population, best_count, population_size):
        
        itr_cnt = 0
        max_itr = 10000
        
        while(itr_cnt < max_itr):
            board_population = self.select(board_population, best_count)
            prev_best_board = board_population[0]
            
            for i in range(random.randint(1,3)):
                crossover_children = self.crossover(board_population,i)
                board_population += crossover_children
                heapq.heapify(board_population)
            
            heapq.heapify(board_population)
            
            while len(board_population) < population_size:
                indx = random.randint(0,len(board_population)-1)
                new_board = self.mutate(board_population[indx])
                heapq.heappush(board_population, new_board)
            
            heapq.heapify(board_population)
            
            self.Converged_board = board_population[0]
            
            if(self.Converged_board.fitness == 0):
                break

            if(self.Converged_board.fitness < prev_best_board.fitness):
                itr_cnt = 0
            else:
                self.Converged_board = prev_best_board
                itr_cnt += 1

            self.Converging_cnt += 1
            
    
if __name__ == "__main__":
    print("\t\tGenetic Algorithm\n\t\t N - Queens\n")
    population_size = 15
    K = min(population_size * 3//4, 5)
    board_length = 8
       
    board_population = []
    
    print("Generating Population ...\n")
    
    while len(board_population) < population_size:
        board = Board_State([random.randint(1,board_length) for i in range(board_length)])
        heapq.heappush(board_population, board)   
    
    print("Converging .....\n")
    
    Final_Solution = Genetic_Solver()
    Final_Solution.GeneticConvergence(board_population, K , population_size) 
    
    print("Iterations took to converge to a Good state : ", Final_Solution.Converging_cnt)
    print()
    print("Final Board : ",Final_Solution.Converged_board)
    print("Fitness     : ", Final_Solution.Converged_board.fitness)
    print()


'''
Output :
                Genetic Algorithm
                 N - Queens
Generating Population ...
Converging .....
Iterations took to converge to a Good state :  221
Final Board :  
        - - 👑 - - - - - 
        - - - - 👑 - - - 
        - 👑 - - - - - - 
        - - - - - - - 👑 
        👑 - - - - - - - 
        - - - - - - 👑 - 
        - - - 👑 - - - - 
        - - - - - 👑 - - 
Fitness     :  0
'''

'''
Output: 
                Genetic Algorithm
                 N - Queens
Generating Population ...
Converging .....
Iterations took to converge to a Good state :  97
Final Board :  
        - - 👑 - - - - - 
        - - - - - - 👑 - 
        - 👑 - - - - - - 
        - - - - - - - 👑 
        - - - - 👑 - - - 
        👑 - - - - - - - 
        - - - 👑 - - - - 
        - - - - - 👑 - - 
Fitness     :  0
'''