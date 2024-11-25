import heapq
import requests

def parse_graph_data(url):
    # Download the file from the URL
    response = requests.get(url)
    response.raise_for_status()  # Check for any errors in the download

    # Read lines from the downloaded file
    lines = response.text.strip().split('\n')
    
    # Parse the first line to get the number of nodes and edges
    number_of_nodes, number_of_edges = map(int, lines[0].strip().split())
    
    # Parse each edge and build the adjacency list
    adjacency_list = {i: [] for i in range(1, number_of_nodes + 1)}
    for line in lines[1:]:
        node1, node2, cost = map(int, line.strip().split())
        adjacency_list[node1].append((cost, node2))
        adjacency_list[node2].append((cost, node1))

    return adjacency_list, number_of_nodes

def prim_mst(adjacency_list, number_of_nodes):
    # Initialize variables for Prim's algorithm
    total_cost = 0
    visited = set()  # Set of nodes that are already in the MST
    min_heap = [(0, 1)]  # Starting with node 1 and a 0 cost edge (arbitrary starting point)

    # Main loop of Prim's algorithm
    while len(visited) < number_of_nodes:
        # Pop the edge with the smallest cost from the heap
        cost, node = heapq.heappop(min_heap)

        # If this node is already visited, continue to the next iteration
        if node in visited:
            continue

        # Add this edge to the MST
        total_cost += cost
        visited.add(node)

        # Add all edges from the current node to the heap
        for edge_cost, neighbor in adjacency_list[node]:
            if neighbor not in visited:
                heapq.heappush(min_heap, (edge_cost, neighbor))

    return total_cost

def main():
    # URL of the input data file
    url = "https://d3c33hcgiwev3.cloudfront.net/_d4f3531eac1d289525141e95a2fea52f_edges.txt?Expires=1730592000&Signature=JCeAkzZ0QZh3iyq36qmTcrf8sE0N5eHGJoMHIwmaS4FtGsTQxydvMcPiZf5-qhXKCcehvitb0Ad1hzfLtEPGER7ATaxjqVhsYZ~Tns9UdJKJ0xroTzXYQ8layCs3MSxVUb8QPvjGRjf0ioXv-xfXP9eR3uOSs4V4suk1wGWTQ0w_&Key-Pair-Id=APKAJLTNE6QMUY6HBC5A"
    
    # Parse the graph data from the URL
    adjacency_list, number_of_nodes = parse_graph_data(url)
    
    # Run Prim's algorithm to find the MST cost
    mst_cost = prim_mst(adjacency_list, number_of_nodes)
    print(mst_cost)

if __name__ == "__main__":
    main()
