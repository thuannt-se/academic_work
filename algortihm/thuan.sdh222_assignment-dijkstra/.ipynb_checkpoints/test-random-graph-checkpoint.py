# import supporting modules
import networkx as nx
import numpy as np

# basic version of dijkstra's algorithm
from naive_dijkstra import naive_dijkstra

# create a weighted simple undirected graph with by networkx
G = nx.erdos_renyi_graph( 1000, 0.01, seed=0 )

# generate weights randomly in U(10,200)
weights = dict()
for e in G.edges:
    weights[e] = {"length": np.random.uniform(10,200)}
nx.set_edge_attributes( G, weights )

# create our graph using an adjacency list representation
# each "node" in our list should be a node name and a distance
graph = dict()
for n in range( G.number_of_nodes() ):
    graph[n] = []
for line in nx.generate_adjlist(G):
    nodes = line.split(" ")
    #A = []
    for a in range(1,len(nodes)):
        graph[int(nodes[0])] += [( int(nodes[a]), G.edges[int(nodes[0]),int(nodes[a])]['length'] )]
        graph[int(nodes[a])] += [( int(nodes[0]), G.edges[int(nodes[0]),int(nodes[a])]['length'] )]
    
# graph is stored in adjacency list as below
#graph = {
#    0: [(1, 1)],
#    1: [(0, 1), (2, 2), (3, 3)],
#    2: [(1, 2), (3, 1), (4, 5)],
#    3: [(1, 3), (2, 1), (4, 1)],
#    4: [(2, 5), (3, 1)]
#}

dist = naive_dijkstra( graph, 0 )
print( dist )
