import pandas as pd
from collections import Counter
from shapely.wkt import loads
from shapely.geometry import Point
import networkx as nx
import matplotlib.pyplot as plt
from math import sin, cos, sqrt, atan2, radians
import folium
import pickle


def haversine_distance(lat1, lon1, lat2, lon2):
    # Convert coordinates to radians
    lat1_rad = radians(lat1)
    lon1_rad = radians(lon1)
    lat2_rad = radians(lat2)
    lon2_rad = radians(lon2)

    # Earth's radius in kilometers
    radius = 6371

    # Calculate the differences between the coordinates
    dlat = lat2_rad - lat1_rad
    dlon = lon2_rad - lon1_rad

    # Apply the Haversine formula
    a = sin(dlat / 2) ** 2 + cos(lat1_rad) * cos(lat2_rad) * sin(dlon / 2) ** 2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))
    distance = radius * c

    return distance


# Read the CSV file without a header row
df = pd.read_csv('directed_graph_BTN2.csv')


# Filter rows with "LINESTRING" in the WKT column, except the first row
point_df = df[df['WKT'].str.contains('POINT')]

# Create an empty list to store all nodes

G = nx.DiGraph()
# Iterate over each row
for _, row in point_df.iterrows():
    node = row['name']
    G.add_node(node)

# Create a folium map centered around the first node
m = folium.Map()

# Filter rows with "LINESTRING" in the WKT column, except the first row
line_df = df[df['WKT'].str.contains('LINESTRING')]

for _, row in line_df.iterrows():
    wkt = row['WKT']
    linestring = loads(wkt)

    if linestring.geom_type == 'LineString':
        coordinates = list(linestring.coords)
        folium.PolyLine(locations=coordinates, color='blue').add_to(m)
        # Loop through the coordinates of the LineString
        for index in range(0, len(linestring.coords) - 1):
            x_start, y_start = linestring.coords[index]
            x_end, y_end = linestring.coords[index + 1]
            # Create a Shapely Point object
            query_start_point = Point(x_start, y_start)
            query_end_point = Point(x_end, y_end)
            found_start_point = point_df[point_df['WKT'].apply(
                lambda g: query_start_point.within(loads(g)))]
            if (found_start_point.shape[0] != 1):
                print(
                    "🚀 ~ file: preprocess_point.py:38 ~ query_start_point:", query_start_point)
                continue

            found_end_point = point_df[point_df['WKT'].apply(
                lambda g: query_end_point.within(loads(g)))]
            if (found_end_point.shape[0] != 1):
                print(
                    "🚀 ~ file: preprocess_point.py:39 ~ query_end_point:", query_end_point)
                continue

            G.add_weighted_edges_from([(found_start_point.iloc[0]['name'],
                                       found_end_point.iloc[0]['name'], haversine_distance(y_start, x_start, y_end, x_end))])

nx.draw(G, with_labels=True)
plt.show()

with open('G.pickle', 'wb') as handle:
    pickle.dump(G, handle, protocol=pickle.HIGHEST_PROTOCOL)

shortest_path = nx.bellman_ford_path(G, 'DHBK', 'DDL', weight='weight')

for i in range(len(shortest_path)-1):
    start_node = shortest_path[i]
    end_node = shortest_path[i+1]

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

print("🚀 ~ file: preprocess_point.py:84 ~ shortest_path:", shortest_path)
