from numpy import Inf
import heapq as hq

# takes the graph and the starting node
# returns a list of distances from the starting node to every other node
# to reduce the number of nested loops => I use priority queue to keep track of all the vertex
# the vertex with shortest distance to root would have the top priority and will be pop out first
@profile
def naive_dijkstra(graph, root):
    n = len(graph)

    # initialize distance list as all infinities
    dist = [Inf for _ in range(n)]
    # set the distance for the root to be 0
    dist[root] = 0
    
    # we use priority queue to control the node and it's distance to root
    pq = [(0, root)]
    
    #pq is not empty, meaning there's still more nodes to consider
    while len(pq) > 0 :
        
        #pop out the lowest distance vertex and process
        curr_distance, curr_vertex = hq.heappop(pq)
        
        #
        if(curr_distance > dist[curr_vertex]):
            continue
        
        for adj_vertex, weight in graph[curr_vertex]:
            distance = curr_distance + weight
            
            if(distance < dist[adj_vertex]):
                dist[adj_vertex] = distance
                hq.heappush(pq, (distance, adj_vertex))
    return dist
