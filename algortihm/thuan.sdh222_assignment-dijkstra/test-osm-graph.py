# import required modules
import osmnx
import networkx as nx

# basic version of dijkstra's algorithm
from optimized_dijkstra import optimized_dijkstra

# a location as a center of the generated graph
place_name = "Ho Chi Minh City University of Technology"

# read the graph from OpenStreetMap and convert it to Networkx data
osmG = osmnx.graph_from_address( place_name, dist = 1000 )
G = nx.Graph( osmG )

# plot the OpenStreetMap graph
osmnx.plot_graph( osmG )

# plot the graph on map
osmnx.folium.plot_graph_folium( osmG )

# Retrieve nodes and edges in GeoPandas
nodes, edges = osmnx.graph_to_gdfs( osmG )

# generate a forward map and reverse map between osmid to ids ranged from 0->#nodes
i = 0
idmap = dict()    # forward map: osmid -> [0,...,n-1]
idrmap = dict()   # reverse map: [0,...,n-1] -> osmid
for n in G.nodes(data=False):
    idmap[n] = i
    idrmap[i] = n
    i = i+1
    
# create a graph compatible to naive_dijkstra's algorithm
# create a graph compatible to naive_dijkstra's algorithm
graph = dict()
for n in range( G.number_of_nodes() ):
    graph[n] = []
for line in nx.generate_adjlist(G):
    nodes = line.split(" ")
    for a in range(1,len(nodes)):
        graph[idmap[int(nodes[0])]] += [( idmap[int(nodes[a])], 
                                         G.edges[int(nodes[0]),int(nodes[a])]['length'] )]
        graph[idmap[int(nodes[a])]] += [( idmap[int(nodes[0])], 
                                         G.edges[int(nodes[0]),int(nodes[a])]['length'] )]

# graph is stored in adjacency list as below
#graph = {
#    0: [(1, 1)],
#    1: [(0, 1), (2, 2), (3, 3)],
#    2: [(1, 2), (3, 1), (4, 5)],
#    3: [(1, 3), (2, 1), (4, 1)],
#    4: [(2, 5), (3, 1)]
#}

# run the naive dijkstra's algorithm
dist = optimized_dijkstra( graph, 1 )
print( dist )


