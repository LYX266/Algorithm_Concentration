"""Dijkstra's shortest-path algorithm"""

import heapq
from collections import defaultdict
import requests

# Define a large value for unreachable distances
INFINITY = 1000000

# Function to load the graph from a URL
def load_graph_from_url(url):
    graph = defaultdict(list)
    response = requests.get(url)
    response.raise_for_status()  # Raise an error for bad responses
    for line in response.text.strip().split('\n'):
        parts = line.strip().split('\t')
        vertex = int(parts[0])
        edges = [edge.split(',') for edge in parts[1:]]
        for neighbor, weight in edges:
            neighbor = int(neighbor)
            weight = int(weight)
            graph[vertex].append((neighbor, weight))
            graph[neighbor].append((vertex, weight))  # Graph is undirected
    return graph

# Dijkstra's algorithm implementation
def dijkstra(graph, source):
    # Initialize distances with INFINITY and set source distance to 0
    distances = {i: INFINITY for i in range(1, 201)}
    distances[source] = 0
    priority_queue = [(0, source)]  # (distance, vertex) pairs

    while priority_queue:
        current_distance, current_vertex = heapq.heappop(priority_queue)

        # If the current distance is already greater than the recorded shortest distance, skip it
        if current_distance > distances[current_vertex]:
            continue

        # Check neighbors of the current vertex
        for neighbor, weight in graph[current_vertex]:
            distance = current_distance + weight
            # Only consider this path if it's better than any previously recorded path
            if distance < distances[neighbor]:
                distances[neighbor] = distance
                heapq.heappush(priority_queue, (distance, neighbor))

    return distances

# Main function to solve the problem
def main():
    # Load the graph from the URL
    url = "https://d3c33hcgiwev3.cloudfront.net/_dcf1d02570e57d23ab526b1e33ba6f12_dijkstraData.txt?Expires=1730332800&Signature=RPxP5skgkccRDZORlJciRwyrngyzoZTEv9QrXyxLSMI6-Uah3YpyP0bVndEwOdx8duSQT0PaSSd2ICfbuAyf8Yk3axnhdZdf9itgf41YJVzBdVEJ9IFUj6PnMSYVuZccB1TgWQYNmdIJaWTmt6muWBIoP5CNOq~YiFSLNVwgXj0_&Key-Pair-Id=APKAJLTNE6QMUY6HBC5A"
    graph = load_graph_from_url(url)
    
    # Run Dijkstra's algorithm from the source vertex 1
    distances = dijkstra(graph, 1)

    # List of vertices for which we need to report distances
    target_vertices = [7, 37, 59, 82, 99, 115, 133, 165, 188, 197]

    # Retrieve distances for the target vertices, defaulting to 1000000 if unreachable
    result = [str(distances[v]) for v in target_vertices]

    # Print the result as a comma-separated string
    print(",".join(result))

if __name__ == "__main__":
    main()
