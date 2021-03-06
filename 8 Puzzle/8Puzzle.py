import copy
from collections import deque
from queue import PriorityQueue
import heapq
state=[]

# -1 denotes a blank space
initial=[[7,2,4],[5,-1,6],[8,3,1]]
goal=[[-1,1,2],[3,4,5],[6,7,8]]

#explored=[]
#discovered=[] 

mydict = {}


def gen_states(state):
    next_states = []
    for i in range(3):
        for j in range(3):
            if(state[i][j] == -1):
                x = i
                y = j
    
    for i,j in [(-1,0),(1,0),(0,1),(0,-1)]:
        temp=copy.deepcopy(state)
        if(x + i >= 0 and x + i <3 and y + j >= 0 and y + j <3):
            temp[x][y], temp[x+i][y+j] = temp[x+i][y+j], temp[x][y]
            next_states.append(temp)
            #res = [tuple(ele) for ele in temp]
            #t = tuple(res)
            #mydict[t]= state
    
    return next_states



print(gen_states(initial))

def trace_path(f):
        """Traces the path taken by any search algorithm using the parent data member of the Puzzle object."""

        
        path = [f]
        #path.append[f]
        res1 = [tuple(ele) for ele in f]
        x=tuple(res1)
        y = mydict[x]
        while y != None:
            path.append(y)
            res2 = [tuple(ele) for ele in y]
            x= tuple(res2)
            y = mydict[x]

       
        return path[::-1]

def bfs(initial):
    discovered = deque()
    explored = deque()
    discovered.append(initial)
    #print(discovered)
#   explored.append(initial)
    while discovered:
        state = discovered.popleft()
        explored.append(state)
       
        #print(explored)
         
        if(state == goal):
            print("Goal")
            return state
        
        for next_state in gen_states(state):
            if(next_state not in explored):	
                discovered.append(next_state)
                explored.append(next_state)
                #print(next_state)
    return None

def heuristics(state):
	h=0
	for i in range(3):
		for j in range(3):
			if state[i][j]==-1:
				continue
			h+= abs(state[i][j] // 3 - i-j // 3) + abs(state[i][j] % 3 - i-j % 3)

	return h


def greedy_bfs(initial):
	path = []
	parent = {}
	res =[tuple(ele) for ele in initial]
	parent[tuple(res)] = None
	explored = []
	discovered = PriorityQueue()

	discovered.put(initial,heuristics(initial))

	while(discovered.qsize()>0):
		state = discovered.get()
		explored.append(state)

		if(state == goal):
			path = trace(parent)
			print("Goal state")
			return path

		for next_state in gen_states(state):
			if(next_state not in explored):
				res =[tuple(ele) for ele in next_state]
				parent[tuple(res)] = state
				discovered.put(next_state,heuristics(next_state))

def trace(parent):
	path = [goal]
	state = goal
	res =[tuple(ele) for ele in state]
	while parent[tuple(res)] != None:
		path.append(parent[tuple(res)])
		state = parent[tuple(res)]
		res =[tuple(ele) for ele in state]
	return path[::-1]
#    if(state == goal):
#        return state
#    next_states = gen_states(state)
#    for new_state in next_states:
#        return dfs(new_state)
print(greedy_bfs(initial))
#print(mydict)
#trace_path(greedy_bfs(initial))
# (next_state not in discovered) and   
    