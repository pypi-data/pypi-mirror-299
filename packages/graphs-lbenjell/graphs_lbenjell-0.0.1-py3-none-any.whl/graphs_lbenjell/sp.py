import sys
from heapq import heappush, heappop

def dijkstra(graph, source):

    dist = {node: sys.maxsize for node in graph}
    dist[source] = 0

    heap = []
    heappush(heap, (0, source))
    path = {node: [] for node in graph}
    
    while heap:
        w, u = heappop(heap)
        
        for v in graph.get(u, {}):
            if w + graph[u][v] < dist[v]:
                dist[v] = w + graph[u][v]
                heappush(heap, (dist[v], v))
                path[v] = path.get(u, []) + [u]
    
    return dist, path

