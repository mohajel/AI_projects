# %% [markdown]
# # In the Name of God
# Name : Mohammad Mohajel Sadegi
# 
# SID  : 810199483
# 

# %% [markdown]
# ## Abstract:
# Implementation of BFS, IDS and A* search 

# %% [markdown]
# ## Importing libraries:

# %%
import copy
from collections import Counter
# from queue import Queue
# import time

# %%


# %% [markdown]
# ## Class state

# %%
class State:
    def __init__(self, rocky_nodes):
        self.position = 0
        self.recipes_seen = []
        self.morids_seen = []
        self.prev_state = None
        self.rocky_nodes = dict.fromkeys(rocky_nodes, 0)
        self.rocky_remain = 0
        self.cost = 0

# %% [markdown]
# ## Class graph:

# %%
class Graph:
    def __init__(self, v ):
        self.v = v
        self.edges = [[] for _ in range(v)]
        self.morids = None #make it dictionary
        self.recipes = []
        self.start_position = 0
        self.rocky_nodes = []


    def add_edge(self, u , v ) :
        self.edges[u].append(v)
        self.edges[v].append(u)

    def is_rocky(self, node ) :
        return (node in self.rocky_nodes)

    def is_recipes(self, node ) :
        return (node in self.recipes)

    def is_morid(self, node ) :
        return (node in list(self.morids.keys()))

    def get_neighbors(self, s ):
        return self.edges[s.position]


# %% [markdown]
# ## Read input and create graph class

# %%
def create_graph(path ) :
    file = open(path, "r")
    n, m = map(int, file.readline().split(" "))
    g = Graph(n)

    for _ in range(m):
        u, v = map(int, file.readline().split(" "))
        g.add_edge(u - 1, v - 1)

    h = int(file.readline())
    rocky_nodes = list(map(int, file.readline().split(" ")))
    rocky_nodes = [x - 1 for x in rocky_nodes]
    g.rocky_nodes = rocky_nodes
    s = int(file.readline())

    morids = {}
    for _ in range(s):
        line = list(map(int, file.readline().split(" ")))
        line = [x - 1 for x in line]
        morids.update({line[0] : line[2:]})
    g.morids = morids
    
    g.start_position = (int(file.readline()) - 1)

    recipes = []
    for recipe in morids.values():
        recipes.extend(recipe)

    recipes = list(dict.fromkeys(recipes)) # Remove Duplicates From a Python List 
    g.recipes = recipes
    return g

g1 = create_graph("input.txt")
g2 = create_graph("input2.txt")
g3 = create_graph("input3.txt")
g4 = create_graph("input4.txt")


# %% [markdown]
# ## Create initial state

# %%
def create_initial_state(g):
    s = State(g.rocky_nodes)
    s.position = g.start_position
    return s

initial_state1 = create_initial_state(g1)
initial_state2 = create_initial_state(g2)
initial_state3 = create_initial_state(g3)
initial_state4 = create_initial_state(g4)
 

# %% [markdown]
# ## Transition module and goal state implementation:

# %%
counter = 0 # remember to initilize it to 0 in begenning

def reached_goal(s , g) :
    return len(g.morids) == len(s.morids_seen)

def transition(s , g, p ):
    global counter
    counter += 1

    # if s.prev_state == None: #initial_state
    #     print(f"start : {s.position}\n")
    # else:
    #     print(f"{s.prev_state.position} => {s.position} \n")

    next_state = copy.deepcopy(s)
    next_state.prev_state = s
    next_state.cost += 1
    if s.rocky_remain != 0:
        next_state.rocky_remain -= 1
    else:
        next_state.position = p
        if g.is_rocky(p):
            next_state.rocky_remain = next_state.rocky_nodes[p]
            next_state.rocky_nodes[p] += 1

        elif(g.is_recipes(p) and p not in s.recipes_seen):
            next_state.recipes_seen.append(p)

        elif(g.is_morid(p) and p not in s.morids_seen and Counter(g.morids[p]) == Counter(s.recipes_seen)):
            next_state.morids_seen.append(p)
            
    # print(f"going to node {next_state.position + 1}, cost:{next_state.cost}")
    return next_state
    

# %% [markdown]
# ## Print_path function:
# to print path after finding it!

# %%
def print_path(final_state) :
    print("PATH::")
    # s = final_state
    # while True:
    #     print(f"{s.position + 1} <== ")
    #     s = s.prev_state
    #     if s.prev_state == None: #s is first node
    #         print(f"{s.position + 1} ")
    #         break
         

# %% [markdown]
# ## BFS implementation:

# %%
def bfs(g, initial_state ):
    q = []
    q.append(initial_state)
    explored = {initial_state, }
    cost = 0
    while 1:
        state = q.pop(0)
        #for test
        if state.cost > cost:
            cost = state.cost
            print(cost)
            # print(f"cost:{cost}")

        for neighbor in g.get_neighbors(state):
            t = transition(state, g, neighbor)
            if t not in explored:
                if reached_goal(t, g):
                    return t
                q.append(t)
                explored.add(t)
            # print(f"{t.prev_state.position + 1} => {t.position + 1} \n")
        # print("\n")    


# def bfs(g, initial_state ):
#     q = [initial_state]
#     # q.append(initial_state)
#     explored = [initial_state,]
#     cost = 0
#     while 1:
#         state = q.pop(0)
#         if reached_goal(state, g):
#             return state

#         #for test
#         if state.cost > cost:
#             cost = state.cost
#             print(f"cost:{cost}")

        
#         states = [transition(state, g, x) for x in g.get_neighbors(state)]
#         new_states = [x for x in states if x not in explored]
#         q.extend(new_states)
#         explored.extend(new_states)


# %% [markdown]
# ### Test1:

# %%
counter = 0
# # start = time.time()
path1 = bfs(g1, initial_state1)
# # end = time.time()
# print(f"time:{end - start}")
# print_path(path1)
# print(f"cost:{path1.cost},")
# print(f"states:{counter},")

# %% [markdown]
# PATH:
# 
#     8 <==  9 <==  11 <==  10 <==  7 <==  5 <==  4 <==  3 <==  1
# 
# |  | MinCost | StatesWatched | MeanTime |
# | --- | --- | --- | --- |
# | BFS | 8 | 9463 | (0.99+1.06+1.015)/3 |

# %% [markdown]
# ### Test2:

# %%
counter = 0
# # start = time.time()
path4 = bfs(g4, initial_state4)
# # end = time.time()
# print(f"time:{end - start}")
# print_path(path4)
# print(f"cost:{path4.cost},")
# print(f"states:{counter},")

# %%


# %%
counter = 0
# # start = time.time()
path1 = bfs(g2, initial_state2)

print("fuck you!")
# # end = time.time()
# print(f"time:{end - start}")
print_path(path1)
# print(f"cost:{path1.cost},")
# print(f"states:{counter},")
# 
# %%
# print(counter)

# %% [markdown]
# ### Test3:

# %%
# counter = 0
# start = time.time()
# path3 = bfs(g3, initial_state3)
# end = time.time()
# print(f"time:{end - start}")
# print_path(path3)
# print(f"cost:{path3.cost},")
# print(f"states:{counter},")

# %% [markdown]
# ## IDS implementation:

# # %%
# def dfs(state , step , g):
#     if reached_goal(state, g):
#         return state
#     if step == 0:
#         return None

#     for neighbor in g.get_neighbors(state):
#         next_state = transition(state, g, neighbor)
#         result = dfs(next_state, step - 1, g)
#         if result != None:
#             return result
#     return None

# def ids(initial_state , , h = 0):
#     while True:
#         h += 1
#         # print(f"h:{h}")

#         result = dfs(initial_state, h, g)
#         if result != None:
#             return result
#         # print(f"cant find in h:{h}")

# counter = 0
# print_path(ids(initial_state2, g2, 12))

# # %% [markdown]
# # ## Examples:

# # %%
# # x = [ [] for _ in range(5)]
# # print(x)

# # %%
# # a = [1, 2, 3]/
# # b = [4 ,5, 6/]
# # a.extend(b)
# # print(a)

# # %%
# # #how map works in python

# # x = [1,2,3,4,5]

# # def funcc(y):
# #     return y - 1

# # i = list(map(funcc, x))
# # print(i)
# # print(x)

# # %%
# # # using global var inside function

# x = 12
# def func():
#     global x
#     x +=3

# func()
# print(x)

# %%
# print("salam", end = " ")
# print("salam")
# print("salam")

# %%
# ll = [1,2,3,4,5]
# print([x - 1 for x in ll ])

# %%
# #queue in python:

# q = Queue()
# q.put(1)
# q.put(2)
# q.put(3)
# # print(1 in q)
# print(q.get())
# print(q.get())
# print(q.get())

# %%
#how to see if elem in list x:

# x = [1,2,3]
# print(12 in x)

# %%
#so None works!
# aa = None

# if aa == 12:
#     print("ok")
# else:
#     print("ok2")

# %%
# aa = [1,2,3]
# bb = [3,2,1]

# Counter(aa) == Counter(bb)

# print(aa)
# print (bb)

# a = 67 

# def func():
#     print(a)

# # x = [12,13,True,"salam"]
# # if x == "salam":
# #     print("yes")
# # print("no")

# # print(range(10))
# func()

# d = {
#     1 : [1,2,3],
#     2 : [1,2,3],
#     9 : [1,2,3],
#     "salam" : 78,
#     4 : [1,2,3],
# }
# d["salam"] += 100
# print(d)

# s = "salam balajan"
# print(s[2:])
# sss = "33"
# b = int(sss.split(" "))
# # print(a)
# print(b)
# type(b)

# %%
# d = {
#     1 : [1,2,3],
#     2 : [1,2,3],
#     9 : [1,2,3],
#     4 : [1,2,3],
# }

# l = list(d.keys())
# print(l)
# print(type(l))
# x = [1,4,"salam", 7]
# print(dict.fromkeys(x, 0))
# len(d)

# for recipe in d.values():
#     print(recipe)
#     print(type(recipe))



# %%
# How deep copy works in python:
# g = Graph(12)
# h = copy.deepcopy(g)
# print(g.v)
# h.v = 33
# print(g.v)


