"""
Computing Strongly Connected Components (SCCs) using Kosaraju's algorithm (DFS)
"""


import requests
from collections import defaultdict, deque
import sys

# Constants
MAX_NODES = 875714

# Graph and Transposed Graph
graph = defaultdict(list)
transposed_graph = defaultdict(list)

# Step 1: Read input from a URL and build both the graph and its transpose
def load_graph_from_url(url):
    response = requests.get(url)
    response.raise_for_status()  # Ensure we notice bad responses
    for line in response.text.strip().split('\n'):
        u, v = map(int, line.strip().split())
        graph[u].append(v)
        transposed_graph[v].append(u)

# Step 2: First DFS pass on the original graph to determine finishing times
def dfs_first_pass(node, visited, finish_stack):
    visited[node] = True
    for neighbor in graph[node]:
        if not visited[neighbor]:
            dfs_first_pass(neighbor, visited, finish_stack)
    finish_stack.append(node)

# Step 3: Second DFS pass on the transposed graph to find SCCs
def dfs_second_pass(node, visited):
    scc_size = 1
    stack = deque([node])
    visited[node] = True
    while stack:
        current = stack.pop()
        for neighbor in transposed_graph[current]:
            if not visited[neighbor]:
                visited[neighbor] = True
                scc_size += 1
                stack.append(neighbor)
    return scc_size

# Kosaraju’s Algorithm to find SCC sizes
def kosaraju():
    # Step 1: Run DFS on the original graph to get finish times
    visited = [False] * (MAX_NODES + 1)
    finish_stack = []
    
    for node in range(1, MAX_NODES + 1):
        if not visited[node] and node in graph:
            dfs_first_pass(node, visited, finish_stack)
    
    # Step 2: Run DFS on the transposed graph in the order of finish times
    visited = [False] * (MAX_NODES + 1)
    scc_sizes = []
    
    while finish_stack:
        node = finish_stack.pop()
        if not visited[node]:
            scc_size = dfs_second_pass(node, visited)
            scc_sizes.append(scc_size)
    
    # Sort SCC sizes in descending order
    scc_sizes.sort(reverse=True)
    return scc_sizes

# Main function
def main():
    # Load the graph from a URL
    load_graph_from_url("https://d3c33hcgiwev3.cloudfront.net/_410e934e6553ac56409b2cb7096a44aa_SCC.txt?Expires=1730332800&Signature=kmSZEL7J22MwNpOLLVAMo6HqILQB7XBR-Ig7GaSpOsyE4KZIZHJcJ6Q21QBOkdl3wDLFitS2lORhRbnzFuVHHaiXPyN0lqvXzGCaLaMkFqed~HI1he4HPv6WhdjsMRDmJMlBR7VWlzPlYMsgeOlp7o7--ortkKQCtZV4vR5r~Kk_&Key-Pair-Id=APKAJLTNE6QMUY6HBC5A")
    
    # Find SCC sizes
    scc_sizes = kosaraju()
    
    # Output the sizes of the 5 largest SCCs
    result = [str(scc_sizes[i]) if i < len(scc_sizes) else "0" for i in range(5)]
    print(",".join(result))

if __name__ == "__main__":
    sys.setrecursionlimit(1000000)  # Increase the recursion limit
    main()
