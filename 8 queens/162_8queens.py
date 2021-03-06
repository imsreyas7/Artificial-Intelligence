class Board:
    """Class to work with the chessboard and its related functions. """
    
    def __init__(self, config):
        """To create a new board configuration with its cost. """
        
        self.config = config
        self.size = len(self.config)
        self.cost = self.find_conflicts()
    
    def __str__(self):
        """To print the board in a formatted manner. """
        
        ret_str = ""
        for pos in self.config:
            for i in range(1, self.size+1):
                if i == pos:
                    ret_str += "👑\t"
                else:
                    ret_str += "❌\t"
            
            ret_str += "\n"
        
        return ret_str
    
    def find_conflicts(self):
        """To find the number of conflicts in the given board configuration. """
        
        conflicts = 0
        
        for i in range(self.size):
            for j in range(i+1, self.size):
                
                if self.config[i] == self.config[j]:         #same row
                    conflicts += 1
                
                elif self.config[i]+i == self.config[j]+j:   #same diagonal
                    conflicts += 1
                    
                elif self.config[i]-i == self.config[j]-j:   #same antidiagonal
                    conflicts += 1
        
        return conflicts

class Solver:
    """Class to solve the 8-Queens Problem given a configuration."""
    
    def find_next_board(self, board):
        """To find the best next best board configuration possible, with minimum cost. """

        next_best_board = board

        for i in range(board.size):
            for j in range(1, board.size + 1):
                if j != board.config[i]:
                    new_config = [x for x in board.config]
                    new_config[i] = j
                    new_board = Board(new_config)

                    if new_board.cost < next_best_board.cost:
                        next_best_board = new_board

        return next_best_board
        
    def hill_climber(self, board):
        """To find a solution to 8-Queens problem without conflicts. """

        while True:
            next_board = self.find_next_board(board)
        
            if next_board.cost == board.cost: #No more improvement
                break
            else:
                board = next_board
                
        return board

if __name__ == "__main__":
    """Driver function to execute the 8-Queens Problem. """
    
    init_config = [4, 3, 2, 5, 4, 3, 2, 3]
    init_board = Board(init_config)
    
    print("\nInitial Board Configuration\n")
    print(init_board)
    print("No. of Conflicts: ", init_board.cost)
    
    s = Solver()
    final_board = s.hill_climber(init_board)
    
    print("\nFinal Board Configuration\n")
    print(final_board)
    print("No. of Conflicts: ", final_board.cost)
    
    init_config = [1, 2, 4, 3, 6, 5, 8, 8]
    init_board = Board(init_config)
    
    print("-----------------------------------")
    print("\nInitial Board Configuration\n")
    print(init_board)
    print("No. of Conflicts: ", init_board.cost)
    
    s = Solver()
    final_board = s.hill_climber(init_board)
    
    print("\nFinal Board Configuration\n")
    print(final_board)
    print("No. of Conflicts: ", final_board.cost)