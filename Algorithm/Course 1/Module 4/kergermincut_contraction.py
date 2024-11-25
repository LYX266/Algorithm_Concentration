# contraction algorithm for min cut

import random
import requests

def parse_graph_from_url(url):
    graph = {}
    response = requests.get(url)
    for line in response.text.strip().split('\n'):
        parts = line.strip().split()
        vertex = int(parts[0])
        edges = list(map(int, parts[1:]))
        graph[vertex] = edges
    return graph

def karger_min_cut(graph):
    while len(graph) > 2:
        u = random.choice(list(graph.keys()))  # randomly select a vertex u
        v = random.choice(graph[u])   # randomly select an adjacent vertex to form an egde
        
        # Merge v into u and remove self-loops
        graph[u].extend(graph[v]) # add edges for v to u
        for vertex in graph[v]:
            graph[vertex].remove(v) # remove v from adjacency
            if vertex != u:
                graph[vertex].append(u) # add u to adjacency
        graph[u] = [x for x in graph[u] if x != u] # remove self loops
        del graph[v] # remove vertex v completely
    
    return len(graph[list(graph.keys())[0]]) 

# conduct 100 iterations and find the minimum of all outputs
def find_min_cut(url, iterations=100):
    min_cut = float('inf')
    for _ in range(iterations):
        graph = parse_graph_from_url(url)
        cut = karger_min_cut(graph)
        if cut < min_cut:
            min_cut = cut
    return min_cut

url = 'https://d3c33hcgiwev3.cloudfront.net/_f370cd8b4d3482c940e4a57f489a200b_kargerMinCut.txt?Expires=1727740800&Signature=YgVc4V-kS1xqYO4gwdAeuG4boUTZKlKTPPmAmpSf7rMPBCwZgCZ-~6HdutAhpJWB8OBXkA1cGQ7CDf68kmni4DpIgrM1gllwsZzleUcWmcb70jggoFuprPAFeB7vB0nxzX0Sh1IFgf2fmFXSywJM5~fBQOpeGHyvC35W~jgrNEA_&Key-Pair-Id=APKAJLTNE6QMUY6HBC5A'
print("Minimum cut:", find_min_cut(url))

