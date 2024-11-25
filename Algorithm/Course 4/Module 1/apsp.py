# Experimented Floyd-Warshall, but Johnson's algorithm is faster.

import requests
import heapq

INF = float('inf')

def bellman_ford(V, edges, src):
    """ Bellman-Ford algorithm to find shortest path from src and detect negative cycles. """
    dist = [INF] * (V + 1)
    dist[src] = 0
    
    for _ in range(V):
        for u, v, w in edges:
            if dist[u] != INF and dist[u] + w < dist[v]:
                dist[v] = dist[u] + w
    
    # Check for negative weight cycles
    for u, v, w in edges:
        if dist[u] != INF and dist[u] + w < dist[v]:
            return None  # Indicates a negative cycle
    
    return dist[:-1]  # Ignore the distance to the auxiliary node

def dijkstra(V, adj_list, src):
    """ Dijkstra's algorithm using a priority queue. """
    dist = [INF] * V
    dist[src] = 0
    pq = [(0, src)]
    
    while pq:
        d, u = heapq.heappop(pq)
        
        if d > dist[u]:
            continue
        
        for v, weight in adj_list[u]:
            if dist[u] + weight < dist[v]:
                dist[v] = dist[u] + weight
                heapq.heappush(pq, (dist[v], v))
    
    return dist

def johnson(V, edges):
    # Step 1: Add an auxiliary node connected to every other node with 0-weight edges
    new_edges = edges + [(V, i, 0) for i in range(V)]
    
    # Step 2: Run Bellman-Ford from the auxiliary node to calculate potentials
    h = bellman_ford(V, new_edges, V)
    if h is None:
        return None  # Indicates a negative cycle
    
    # Step 3: Reweight edges to eliminate negative weights
    reweighted_edges = []
    adj_list = [[] for _ in range(V)]
    for u, v, w in edges:
        new_weight = w + h[u] - h[v]
        reweighted_edges.append((u, v, new_weight))
        adj_list[u].append((v, new_weight))
    
    # Step 4: Run Dijkstra's algorithm from each vertex
    shortest_shortest_path = INF
    for u in range(V):
        dist = dijkstra(V, adj_list, u)
        for v in range(V):
            if u != v and dist[v] != INF:
                original_distance = dist[v] - h[u] + h[v]
                shortest_shortest_path = min(shortest_shortest_path, original_distance)
    
    return shortest_shortest_path if shortest_shortest_path != INF else None

def process_graph_data(url):
    response = requests.get(url)
    data = response.text.strip().splitlines()
    
    # Read number of vertices and edges
    first_line = data[0].split()
    V = int(first_line[0])
    E = int(first_line[1])
    
    edges = []
    for line in data[1:]:
        u, v, w = map(int, line.split())
        # Convert to 0-based indexing for easier matrix handling
        edges.append((u - 1, v - 1, w))
    
    # Run Johnson's algorithm for this graph
    return johnson(V, edges)

def main(urls):
    for index, url in enumerate(urls):
        result = process_graph_data(url)
        if result is None:
            print(f"Graph {index + 1}: Negative cycle detected")
        else:
            print(f"Graph {index + 1}: Shortest shortest path is {result}")


urls = [
    "https://d3c33hcgiwev3.cloudfront.net/_6ff856efca965e8774eb18584754fd65_g1.txt?Expires=1731369600&Signature=RKs1arxHdQPpDxQdTiSni6EmgxjR7SVnW6t9LNfiYCkYTHVMXT0eicH9VDrHCq5lmf77An2QGrUm50mo3-9jktE90MskQ15Tdvz5IXUK3m21bVioab3OaNKHKSHLdeGH7f29O2psy3fq4SxGG9~QAugHC4fTegfCQcbmezLh5FQ_&Key-Pair-Id=APKAJLTNE6QMUY6HBC5A",
    "https://d3c33hcgiwev3.cloudfront.net/_6ff856efca965e8774eb18584754fd65_g2.txt?Expires=1731369600&Signature=NUW3-c6aF4IFHa5Nn5BswNflE2g0frJ1NfzazSrfrurGMpFSD~YgSQT4wwqjwZ66yJatg~lmYLXnRG1k2nJ7Wy74k7MIKtfvgEvRW8k6fGM~X~RVg3h5jOPpheC6uAsDpnNJzQ4L8DZ21GAQXeLFq4VX4ecE8eK5aFhyBqQnAno_&Key-Pair-Id=APKAJLTNE6QMUY6HBC5A",
    "https://d3c33hcgiwev3.cloudfront.net/_6ff856efca965e8774eb18584754fd65_g3.txt?Expires=1731369600&Signature=gIIFpBZ620wFZ6voa1Gs7sz91wu3EOI-5r1wchVZGjrV5XUZXruLz~iw5OPWitEzbiDUpmN~T4B7YUMyyY5xSr0xWTFBEJcGW0UAyQti0q2GXosfh8oVNwPbkVIjkGr46moACcW9skgfPiU5ZR6KGjukYpPv~-mjF9JXtBHCkwY_&Key-Pair-Id=APKAJLTNE6QMUY6HBC5A"
]
main(urls)
