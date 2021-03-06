#done by - Venkataraman-192
#got some help from  siddharth-150 #

from search import Problem
from collections import deque
import heapq
import math
from shapely.geometry import LineString,Polygon

class PathSearch(Problem):
    initial = None
    goal = None
    polygons = None
    pointList = None
    verticesCount = None
    adj_mat = None
    
    def __init__(self, initial, goal, polygons):
        '''
        This class is a subclass of Problem class in search.py
        Initialize the space with initial, goal and polygons.
        Then unzip the polygons into set of vertices and save it as 
        set of nodes with inital and final states in pointList. 
        Edges are formed between these nodes by building an adjacency matrix 
        '''
        
        self.initial = initial
        self.goal = goal
        self.polygons = polygons
        self.pointList = []
        
        self.pointList.append(self.initial)
        for polygon in self.polygons:
            for point in polygon:
                self.pointList.append(point)
        self.pointList.append(self.goal)
        
        self.verticesCount = len(self.pointList)
        self.adj_mat = self.generate_adj_mat() 
        super().__init__(initial,goal)
    
    def isedge(self, polygon, points):
        '''
        This function checks whether the points form an edge of a polygon,
        When the points form an edge of a polygon we say that they dont
        actually intersect with the polygon rather glides through the 
        surface of the polygon.
        '''
        
        n = len(polygon)
        for i in range(n):
            if(points[0] == polygon[i] and points[1] == polygon[(i+1)%n]) or \
                (points[1] == polygon[i] and points[0] == polygon[(i+1)%n]):
                    return True
        
        return False
    
    def generate_adj_mat(self):
        '''
        This function forms the adjaceny matrix using a naive algorithm from
        the set of points/nodes. the adjacency matrix value is infinity if we 
        cannot establish a direct edge connection between two nodes. else the 
        euclidan distance is taken as the edge weight in adjacency matrix. 
        '''
        
        adj = [[math.inf for j in range(self.verticesCount)] for i in range(self.verticesCount)]
        polygon_list = [Polygon(poly) for poly  in self.polygons]
        
        for pos1 in range(self.verticesCount):
            for pos2 in range(self.verticesCount):
                
                point1 = self.pointList[pos1]
                point2 = self.pointList[pos2]
                
                isIntersecting = False
                line = LineString([point1,point2])
                
                for ind, polygon in enumerate(polygon_list):
                    intersectingPoints = list(polygon.intersection(line).coords)
                    
                    if(len(intersectingPoints) > 1):
                        if(len(intersectingPoints)==2 and self.isedge(self.polygons[ind],intersectingPoints)):
                            continue
                        else:
                            isIntersecting = True
                            break
                
                if isIntersecting == False:
                    adj[pos1][pos2] = self.EuclideanDistance(point1,point2)
        return adj      
    
    
    def EuclideanDistance(self,point1, point2):
        '''
        Takes in two points and return the Euclidean distance between the two
        given points
        '''
        
        return round(((point1[0]-point2[0])**2 + (point1[1]-point2[1])**2  )**0.5,2)
    
    def next_states(self, src):
        '''
        This functions returns a set of nodes that can be directly with the help of
        adjacency matrix generated, The function returns all those nodes(dest) other than 
        src that has an finite value in adjacency matrix.
        '''
        
        return [dest for dest in range(self.verticesCount) if(self.adj_mat[src][dest] != math.inf and src != dest)]
                    
    def goal_test(self,state):
        '''
        This function checks whether the provided state is goal state or not
        '''
        
        return self.pointList[state] == self.goal
        
    def edge_cost(self, state1, state2):
        '''
        This function return the weight of the edge between two nodes provided
        '''
        
        return self.adj_mat[state1][state2]
    
    def value(self, state):
        '''
        This function can be used as an Heuristic for Informed searches or 
        Local search algorithms. It return the Euclidean distance between 
        the given node and the goal node.
        '''
        
        point  = self.pointList[state]
        return self.EuclideanDistance(point, self.goal)
    
    def set_path(self, goal, parent):
        '''
        Generates the path list to reach from source to destination
        '''
        
        start = goal
        path = []
        while start:
            path.append(start)
            start = parent[start]
        path.append(0)
        path = path[::-1]
        return path
    
    def total_cost(self, path):
        '''
        Takes in the path and return the total cost of the path
        '''
        
        return sum([self.edge_cost(path[i],path[i+1]) for i in range(len(path)-1)])
    
    def bfs(self, verbose=False):
        parent = dict()
        discovered = deque()
        explored = set()
        
        discovered.append(0)
        explored.add(0)
        
        while discovered:
            if verbose:
                print('Queue : ', discovered)
            state = discovered.popleft()
            for next_state in self.next_states(state):
                if self.goal_test(next_state):
                    parent[next_state] = state
                    path = self.set_path(next_state, parent)
                    return path, self.total_cost(path)
                elif next_state not in explored:
                    explored.add(next_state)
                    discovered.append(next_state)
                    parent[next_state] = state
        
        return None, math.inf
    
    def gbfs(self, verbose=False):
        parent = dict()
        discovered = []
        explored = set()
        
        discovered.append((self.value(0), 0))
        
        while discovered:
            if verbose:
                print('Discovered ', len(discovered), ' nodes')
            val, state = heapq.heappop(discovered)

            if state in explored:
                continue
            
            explored.add(state)
            
            if self.goal_test(state):
                path = self.set_path(state, parent)
                return path, self.total_cost(path)
            
            for next_state in self.next_states(state):
                if next_state not in explored:
                    parent[next_state] = state
                    heapq.heappush(discovered, (self.value(next_state), next_state))
        
        return None, math.inf
    
    def a_star(self, verbose=False):
        parent = dict()
        discovered = []
        explored = set()
        back_cost = dict()
        
        back_cost[0] = 0
        discovered.append((self.value(0), 0))
        
        while discovered:
            if verbose:
                print('Discovered ', len(discovered), ' nodes')
            val, state = heapq.heappop(discovered)

            if state in explored:
                continue
            
            explored.add(state)
            
            if self.goal_test(state):
                path = self.set_path(state, parent)
                return path, self.total_cost(path)
            
            for next_state in self.next_states(state):
                if next_state not in explored:
                    reduced  = False
                    tentative_cost = back_cost[state] + self.edge_cost(state,next_state) + self.value(next_state)

                    if next_state not in back_cost or back_cost[state] + self.edge_cost(state,next_state) < back_cost[next_state]:
                        reduced = True
                        back_cost[next_state] = back_cost[state] + self.edge_cost(state,next_state)
                        
                        if next_state not in [i[1] for i in discovered]:
                            parent[next_state] = state
                            heapq.heappush(discovered, (tentative_cost, next_state))
                        elif reduced:
                            ind = ([i[1] for i in discovered]).index(next_state)
                            discovered[ind] = (tentative_cost, next_state)
                            heapq.heapify(discovered)
        
        return None, math.inf
    