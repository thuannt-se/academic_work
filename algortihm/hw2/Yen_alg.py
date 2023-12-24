from heapq import heappush, heappop
from itertools import count

import networkx as nx

def k_shortest_paths(G, source, target, k=1, weight='weight'):
    if source == target:
        return ([0], [[source]]) 
    
    # Step 1: Calculate the shortest path using any shortest path algorithm, this code use Dijkstra
    length, path = nx.single_source_dijkstra(G, source, target=None, weight=weight)
    if target not in length:
        raise nx.NetworkXNoPath("node %s not reachable from %s" % (source, target))
        
    lengths = [length[target]]
    paths = [path[target]]
    c = count()        
    B = []                        
    G_original = G.copy()    
    
    #Step 2: Iteratively find the next K -1 shortest paths
    for i in range(1, k):
        #Step 3: Generate potential candidate paths
        for j in range(len(paths[-1]) - 1):            
            spur_node = paths[-1][j]
            root_path = paths[-1][:j + 1]
            
            #Step 4: Remove edges
            edges_removed = []
            for c_path in paths:
                if len(c_path) > j and root_path == c_path[:j + 1]:
                    u = c_path[j]
                    v = c_path[j + 1]
                    if G.has_edge(u, v):
                        edge_attr = G.adj[u][v]
                        G.remove_edge(u, v)
                        edges_removed.append((u, v, edge_attr))
            
            for n in range(len(root_path) - 1):
                node = root_path[n]
                # out-edges
                G_copy = G.copy()
                for u, v, edge_attr in G_copy.edges(node, data=True):
                    G.remove_edge(u, v)
                    edges_removed.append((u, v, edge_attr))
            
            #Step 5: Calculate spur path
            spur_path_length, spur_path = nx.single_source_dijkstra(G, spur_node, target=None, weight=weight)            

            #Step 6: Combine root and spur paths
            if target in spur_path and spur_path[target]:
                total_path = root_path[:-1] + spur_path[target]
                total_path_length = get_path_length(G_original, root_path, weight) + spur_path_length[target]                
                heappush(B, (total_path_length, next(c), total_path))
            
            #Step 7: Restore removed edges
            for e in edges_removed:
                u, v, edge_attr = e
                G.add_edge(u, v, weight = edge_attr[weight])
        
        
        #Step 8: Select the best candidate path
        if B:
            B.sort()
            while True:
                (l, _, p) = heappop(B)
                if p not in paths:
                    break
            lengths.append(l)
            paths.append(p)
        else:
            print ('not B once')
            break
    
    return (lengths, paths)

def get_path_length(G, path, weight='weight'):
    length = 0
    if len(path) > 1:
        for i in range(len(path) - 1):
            u = path[i]
            v = path[i + 1]
            
            if G.has_edge(u, v):
                edge_attr = G.adj[u][v]
                length += edge_attr[weight]
    
    return length   

import pickle
import folium
import pandas as pd
from shapely.wkt import loads
import time
# Read the CSV file without a header row
df = pd.read_csv('directed_graph_BTN2.csv')

# Filter rows with "LINESTRING" in the WKT column, except the first row
point_df = df[df['WKT'].str.contains('POINT')]

with open('G.pickle', 'rb') as handle:
    G = pickle.load(handle)

# Run Bellman-Ford algorithm from node 'A'
source_node = 'DHBK'
destination = 'DDL'

start_time = time.time()
distances, paths = k_shortest_paths(G, source_node, destination, 2)
print("--- %s seconds ---" % (time.time() - start_time))

# Add markers for the source and destination nodes
source_geometry = loads(point_df[point_df['name'] == source_node]['WKT'].iloc[0])
destination_geometry = loads(point_df[point_df['name'] == destination]['WKT'].iloc[0])

source_lat, source_lon = source_geometry.y, source_geometry.x
destination_lat, destination_lon = destination_geometry.y, destination_geometry.x


print(distances)
for path in paths:
    print(path)

for j in range(len(paths)):
    m = folium.Map(location=[source_lat, source_lon], zoom_start=12)

    folium.Marker(
        location=[source_lat, source_lon],
        icon=folium.Icon(color='green', icon='play')
    ).add_to(m)

    folium.Marker(
        location=[destination_lat, destination_lon],
        icon=folium.Icon(color='red', icon='stop')
    ).add_to(m)

    for i in range(len(paths[j])-1):
        start_node = paths[j][i]
        end_node = paths[j][i+1]

        start_geometry = loads(point_df[point_df['name'] == start_node]['WKT'].iloc[0])
        end_geometry = loads(point_df[point_df['name'] == end_node]['WKT'].iloc[0])

        start_lat, start_lon = start_geometry.y, start_geometry.x
        end_lat, end_lon = end_geometry.y, end_geometry.x

        folium.PolyLine(
            locations=[[start_lat, start_lon], [end_lat, end_lon]],
            color='red',
            weight=4
        ).add_to(m)

    m.save('map_Yen_'+str(j+1)+'.html')
