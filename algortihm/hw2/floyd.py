import math
import networkx as nx

def floyd_warshall_paths(g, verbose=False):
    #start_time = timeit.default_timer()
    G_number = nx.convert_node_labels_to_integers(g)

    edges = G_number.edges(data=True)
    vertices = list(G_number.nodes())
    n_vertices = len(vertices)
    
    # Init dist matrix
    dist = [[math.inf for j in range(n_vertices)] for i in range(n_vertices)]
    path = [[None for j in range(n_vertices)] for i in range(n_vertices)]
    
    for (u, v, w) in edges:
        u = u - 1
        v = v - 1
        w = w['weight']
        dist[u][v] = w
        path[u][v] = v + 1
    
    for v in range(n_vertices):
        dist[v][v] = 0
        path[v][v] = v + 1
    
    if verbose:
        print('>> run floyd-warshall algorithm')
        
    for k in range(n_vertices):
        for i in range(n_vertices):
            for j in range(n_vertices):
                
                if dist[i][j] > dist[i][k] + dist[k][j]:
                    dist[i][j] = dist[i][k] + dist[k][j]
                    path[i][j] = path[i][k]
                    
                    if verbose:
                        print('   update edge (', i, ',', j, '), value:', dist[i][j])
    
    # Elapsed time
    #if verbose:
        #elapsed = (timeit.default_timer() - start_time) * 1000
        #print('>> elapsed time', elapsed, 'ms')
    
    # Return nodes and dist matrix
    return {'nodes': vertices, 'dist': dist, 'path': path}

def get_shortest_path(paths, u, v):
    
    # Validation
    if paths[u - 1][v - 1] is None:
        return []
    
    # Build the shortest path
    path = [u]
    while u != v:
        u = paths[u - 1][v - 1]
        path.append(u)
    
    return path

import pickle
import folium
import pandas as pd
from shapely.wkt import loads
# Read the CSV file without a header row
df = pd.read_csv('directed_graph_BTN2.csv')

# Filter rows with "LINESTRING" in the WKT column, except the first row
point_df = df[df['WKT'].str.contains('POINT')]

with open('G.pickle', 'rb') as handle:
    G = pickle.load(handle)

# Run Bellman-Ford algorithm from node 'A'
source_node = 'DHBK'
destination = 'DDL'

import time
start_time = time.time()
sol = floyd_warshall_paths(G)
elapsed_time = time.time() - start_time
print("Execution time of Floyd Warshall:", elapsed_time, "seconds")

#print (sol)

mapping = list(G.nodes())

path = get_shortest_path(sol['path'], mapping.index('DHBK'), mapping.index('DDL'))

path_loc = []
for num in path:
    path_loc.append(mapping[num])
print (path_loc)

# Add markers for the source and destination nodes
source_geometry = loads(point_df[point_df['name'] == source_node]['WKT'].iloc[0])
destination_geometry = loads(point_df[point_df['name'] == destination]['WKT'].iloc[0])

source_lat, source_lon = source_geometry.y, source_geometry.x
destination_lat, destination_lon = destination_geometry.y, destination_geometry.x

m = folium.Map(location=[source_lat, source_lon], zoom_start=12)

m = folium.Map(location=[source_lat, source_lon], zoom_start=12)

folium.Marker(
    location=[source_lat, source_lon],
    icon=folium.Icon(color='green', icon='play')
).add_to(m)

folium.Marker(
    location=[destination_lat, destination_lon],
    icon=folium.Icon(color='red', icon='stop')
).add_to(m)

for i in range(len(path_loc)-1):
    start_node = path_loc[i]
    end_node = path_loc[i+1]

    start_geometry = loads(point_df[point_df['name'] == start_node]['WKT'].iloc[0])
    end_geometry = loads(point_df[point_df['name'] == end_node]['WKT'].iloc[0])

    start_lat, start_lon = start_geometry.y, start_geometry.x
    end_lat, end_lon = end_geometry.y, end_geometry.x

    folium.PolyLine(
        locations=[[start_lat, start_lon], [end_lat, end_lon]],
        color='red',
        weight=4
    ).add_to(m)

m.save('map_Floyd' +'.html')
