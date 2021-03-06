import copy
import queue
import heapq
import math
import datetime
import itertools

class Game(object):

    def __init__(self):
        self.visitSet = set()
        self.path = []
        self.expandedList = []
        self.paths = []
        self.row = [0, 0, -1, 1]
        self.col = [1, -1, 0, 0]
        self.maxSearchDepth = 0
        self.bfsPath = {}
    
    def createChild(self, zi, zj, ei, ej, puzzle):
        newPuzzle = copy.deepcopy(puzzle)
        newPuzzle[zi][zj], newPuzzle[ei][ej] = newPuzzle[ei][ej], newPuzzle[zi][zj]
        return newPuzzle

    def addToVisitSet(self, puzzle):
        keyPuzzle = tuple(tuple(x) for x in puzzle)
        self.visitSet.add(keyPuzzle)

    def isVisited(self, puzzle):
        keyPuzzle = tuple(tuple(x) for x in puzzle)
        return keyPuzzle in self.visitSet

    def isFinalState(self, puzzle):
        return puzzle == [ [0,1,2], [3,4,5], [6,7,8] ]
    
    def addToPath(self, puzzle):
        self.path.append(puzzle)

    def addToExpandedList(self, puzzle):
        self.expandedList.append(puzzle)
    
    def addToPaths(self, puzzle):
        self.paths.append(puzzle)
    
    def isValidIdx(self, i, j):
        return i >= 0 and i <= 2 and j >= 0 and j <= 2
    
    def getEIdx(self, puzzle, e):
        zi = -1
        zj = -1
        i = -1
        j=-1
        for r in puzzle:
            i+=1
            j=-1
            for c in r:
                j+=1
                if c == e:
                    zi, zj = i, j
                    break
        return zi, zj



        return total


    def hasChildren(self, puzzle):
        zi, zj = game.getEIdx(puzzle, 0)
        for i in range(4):
            newzi = zi + game.row[i]
            newzj = zj + game.col[i]
            if game.isValidIdx(newzi, newzj):
                p = game.createChild(zi, zj, newzi, newzj, puzzle)
                if game.isVisited(p) == False:
                    return True
        return False
    
    def addToPathMap(self, key, value):
        keyPuzzle = tuple(tuple(x) for x in key)
        valuePuzzle = tuple(tuple(x) for x in value)
        self.bfsPath[keyPuzzle] = valuePuzzle

    def setPath(self, state):
        goalState = tuple(tuple(x) for x in state)
        st = goalState
        print(st)
        while st in self.bfsPath:
            self.path.append(st)
            st = self.bfsPath[st]
            print(st)
        self.path.reverse()

    def isSolvable(self, puzzle):
        array = list(itertools.chain.from_iterable(puzzle))
        print(array)
        invCount = 0
        for i in range(8):
            for j in range(i + 1, 9):
                if array[j] != 0 and array[i] != 0 and array[i] > array[j]:
                    invCount += 1
        print("cnt:",invCount)
        return invCount % 2 == 0


class State(object):    
    def __init__(self, puzz, val):
        self.puzzle = puzz
        self.value = val
        self.distance = 0

    def __lt__(self, other):
        return self.value < other.value

    def _eq_(self, other):
        return self.puzzle == other.puzzle

def bfs(puzzle, game):
    frontier = queue.Queue()
    frontier.put(puzzle)

    while frontier.empty() == False:
        state = frontier.get()

        if game.isVisited(state) == True:
            continue

        game.addToVisitSet(state)
        game.addToExpandedList(state)

        if game.isFinalState(state):
            game.setPath(state)
            return True

        zi, zj = game.getEIdx(state,0)

        for i in range(4):
            newzi = zi + game.row[i]
            newzj = zj + game.col[i]
            if game.isValidIdx(newzi, newzj):
                p = game.createChild(zi, zj, newzi, newzj, state)
                frontier.put(p)
                if game.isVisited(p) == False:
                    game.addToPathMap(p, state)

    return False


#puzz = [[0,1,2], [3,4,5], [6,7,8]]
puzz = [[7,2,4], [5,0,6], [8,3,1]]
game = Game()

if game.isSolvable(puzz):
    print(puzzle)
    zi, zj = game.getEIdx(puzz,0)
    cost = 0
    

    a = datetime.datetime.now()
    print(bfs(puzz,game))
    b = datetime.datetime.now()
    c = b-a
    print(c.total_seconds())
    print("-----")
    print(game.path.pop())
else:
    print("unsolvable")


'''
OUTPUT

[7, 2, 4, 5, 0, 6, 8, 3, 1]
cnt: 16
[[7,2,4], [5,0,6], [8,3,1]]

((0, 1, 2), (3, 4, 5), (6, 7, 8))
((3, 1, 2), (0, 4, 5), (6, 7, 8))
((3, 1, 2), (6, 4, 5), (0, 7, 8))
((3, 1, 2), (6, 4, 5), (7, 0, 8))
((3, 1, 2), (6, 0, 5), (7, 4, 8))
((3, 0, 2), (6, 1, 5), (7, 4, 8))
((3, 2, 0), (6, 1, 5), (7, 4, 8))
((3, 2, 5), (6, 1, 0), (7, 4, 8))
((3, 2, 5), (6, 0, 1), (7, 4, 8))
((3, 2, 5), (6, 4, 1), (7, 0, 8))
((3, 2, 5), (6, 4, 1), (7, 8, 0))
((3, 2, 5), (6, 4, 0), (7, 8, 1))
((3, 2, 5), (6, 0, 4), (7, 8, 1))
((3, 2, 5), (0, 6, 4), (7, 8, 1))
((0, 2, 5), (3, 6, 4), (7, 8, 1))
((2, 0, 5), (3, 6, 4), (7, 8, 1))
((2, 5, 0), (3, 6, 4), (7, 8, 1))
((2, 5, 4), (3, 6, 0), (7, 8, 1))
((2, 5, 4), (3, 0, 6), (7, 8, 1))
((2, 5, 4), (0, 3, 6), (7, 8, 1))
((2, 5, 4), (7, 3, 6), (0, 8, 1))
((2, 5, 4), (7, 3, 6), (8, 0, 1))
((2, 5, 4), (7, 0, 6), (8, 3, 1))
((2, 0, 4), (7, 5, 6), (8, 3, 1))
((0, 2, 4), (7, 5, 6), (8, 3, 1))
((7, 2, 4), (0, 5, 6), (8, 3, 1))
((7, 2, 4), (5, 0, 6), (8, 3, 1))
True
73.365375
-----
((0, 1, 2), (3, 4, 5), (6, 7, 8))
'''


