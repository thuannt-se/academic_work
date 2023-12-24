def bellman_ford(graph, source):
    distances = {node: float('inf') for node in graph.nodes}
    distances[source] = 0
    predecessors = {node: None for node in graph.nodes}

    for _ in range(len(graph.nodes) - 1):
        for u, v, weight in graph.edges.data('weight'):
            if distances[u] + weight < distances[v]:
                distances[v] = distances[u] + weight
                predecessors[v] = u

    # Check for negative cycles
    for u, v, weight in graph.edges.data('weight'):
        if distances[u] + weight < distances[v]:
            raise ValueError("Graph contains a negative-weight cycle")

    paths = {}
    for node in graph.nodes:
        path = []
        current_node = node
        while current_node is not None:
            path.insert(0, current_node)
            current_node = predecessors[current_node]
        paths[node] = path

    return distances, paths

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
distances, paths = bellman_ford(G, source_node)
elapsed_time = time.time() - start_time
print("Execution time of Bellman Ford:", elapsed_time, "seconds")
print("Distance:", distances[destination], "km")

# Add markers for the source and destination nodes
source_geometry = loads(point_df[point_df['name'] == source_node]['WKT'].iloc[0])
destination_geometry = loads(point_df[point_df['name'] == destination]['WKT'].iloc[0])

source_lat, source_lon = source_geometry.y, source_geometry.x
destination_lat, destination_lon = destination_geometry.y, destination_geometry.x

m = folium.Map(location=[source_lat, source_lon], zoom_start=12)

folium.Marker(
    location=[source_lat, source_lon],
    icon=folium.Icon(color='green', icon='play')
).add_to(m)

folium.Marker(
    location=[destination_lat, destination_lon],
    icon=folium.Icon(color='red', icon='stop')
).add_to(m)

print(paths[destination])

for i in range(len(paths[destination])-1):
    start_node = paths[destination][i]
    end_node = paths[destination][i+1]

    start_geometry = loads(point_df[point_df['name'] == start_node]['WKT'].iloc[0])
    end_geometry = loads(point_df[point_df['name'] == end_node]['WKT'].iloc[0])

    start_lat, start_lon = start_geometry.y, start_geometry.x
    end_lat, end_lon = end_geometry.y, end_geometry.x

    folium.PolyLine(
        locations=[[start_lat, start_lon], [end_lat, end_lon]],
        color='red',
        weight=4
    ).add_to(m)

m.save('map.html')
