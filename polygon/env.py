'''
Environment for path finding robot with start location, end location, polygons in-between blocking the path
'''
import math
import random
import itertools

def seq(start, end, step):
    assert(step != 0)
    sample_count = int(abs(end - start) / step)
    return itertools.islice(itertools.count(start, step), sample_count)


class point:
    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y
        self.parent = None
        self.g = 0
    
    def dist(self, p2) -> int:
        dx = self.x - p2.x
        dy = self.y - p2.y
        return math.sqrt(math.pow(dx,2) + math.pow(dy, 2))
    
    def __eq__(self, p2):
        if (self.x == p2.x and self.y == p2.y):
            return True
        return False
    
    @staticmethod
    def genrand(limx: tuple, limy: tuple):
        limx1, limx2 = limx
        limy1, limy2 = limy
        x = random.randint(limx1, limx2)
        y = random.randint(limy1, limy2)
        return point(x, y)
    
    def __str__(self):
        return str(self.x) + str(self.y)
    
    def __hash__(self):
        return hash(str(self))



class polygon:
    def __init__(self, points):
        self.points = points

    def inside(self, x: int, y: int) -> bool:
        vals = []
        for i in range(len(self.points) - 1):
            x1, y1 = self.points[i].x, self.points[i].y
            x2, y2 = self.points[i+1].x, self.points[i+1].y

            A = -(y2-y1)
            B = x2 - x1
            C = -(A*x1 + B*y1)

            vals.append(A*x + B*y + C)
        
        x1, y1 = self.points[len(self.points) - 1].x, self.points[len(self.points) - 1].y
        x2, y2 = self.points[0].x, self.points[0].y
        A = -(y2-y1)
        B = x2 - x1
        C = -(A*x1 + B*y1)
        vals.append(A*x + B*y + C)
        
        t1 = all(d>0 for d in vals)
        t2 = all(d<0 for d in vals)
        return t1 or t2

class line:
    def __init__(self, p1, p2):
        self.x1 = p1.x
        self.y1 = p1.y
        self.x2 = p2.x
        self.y2 = p2.y
    
    def gety(self, x):
        m = (self.y2 - self.y1) / (self.x2 - self.x1)
        y = m * (x-self.x1) + self.y1
        return y
    
    def isinside(self, polygon):
        if (self.x1 != self.x2):
            for x in seq(min(self.x1, self.x2), max(self.x2, self.x1) + 1, 0.1):
                y = self.gety(x)
                if (polygon.inside(x, y)):
                    return True
            return False
        else:
            for y in seq(min(self.y1, self.y2), max(self.y1, self.y2) + 1, 0.1):
                if (polygon.inside(self.x1, y)):
                    return True
            return False

class grid:
    def __init__(self, m: int, n: int, polygons, start: point, goal: point):
        self.m = m
        self.n = n
        self.polygons = polygons
        self.start = start
        self.goal = goal
        self.points = []
        for i in polygons:
            for j in i.points:
                self.points.append(j)
        self.points.append(goal)

    def inside(self, l):
        for polygon in self.polygons:
            if (l.isinside(polygon)):
                return True
        return False

    
    def getActions(self, state):
        next_states = []

        for point in self.points:
            if point != state:
                if state == point:
                    continue
                l = line(state, point)
                if not self.inside(l):
                    next_states.append(point)
        
        return next_states
    
