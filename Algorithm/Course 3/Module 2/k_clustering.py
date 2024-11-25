import requests

class UnionFind:
    def __init__(self, size):
        self.parent = list(range(size))
        self.rank = [1] * size
        self.count = size  # Keeps track of the number of components

    def find(self, p):
        if self.parent[p] != p:
            self.parent[p] = self.find(self.parent[p])  # Path compression
        return self.parent[p]

    def union(self, p, q):
        rootP = self.find(p)
        rootQ = self.find(q)

        if rootP != rootQ:
            # Union by rank
            if self.rank[rootP] > self.rank[rootQ]:
                self.parent[rootQ] = rootP
            elif self.rank[rootP] < self.rank[rootQ]:
                self.parent[rootP] = rootQ
            else:
                self.parent[rootQ] = rootP
                self.rank[rootP] += 1
            self.count -= 1
            return True
        return False

def parse_graph_data(url):
    response = requests.get(url)
    response.raise_for_status()  # Check for any errors in the download
    lines = response.text.strip().split('\n')
    
    # Parse the number of nodes
    number_of_nodes = int(lines[0].strip())
    
    # Parse each edge
    edges = []
    for line in lines[1:]:
        node1, node2, cost = map(int, line.strip().split())
        edges.append((cost, node1 - 1, node2 - 1))  # Convert to zero-based indexing
    
    return edges, number_of_nodes

def maximum_spacing_clustering(edges, number_of_nodes, k):
    # Sort edges by their cost in ascending order
    edges.sort()

    uf = UnionFind(number_of_nodes)

    # Process edges in ascending order until we have exactly k clusters
    for cost, node1, node2 in edges:
        # Only add edge if it connects two different components
        if uf.union(node1, node2):
            # If we have exactly k clusters, stop adding edges
            if uf.count == k:
                # Find the next smallest edge that connects two different clusters
                for next_cost, next_node1, next_node2 in edges:
                    if uf.find(next_node1) != uf.find(next_node2):
                        return next_cost  # This is the maximum spacing

    return None  # Should never reach here if input is valid

def main():
    url = "https://d3c33hcgiwev3.cloudfront.net/_fe8d0202cd20a808db6a4d5d06be62f4_clustering1.txt?Expires=1730678400&Signature=YLmCdD8278sGP59jpo7kKDep9TeR9I6JZml2k8ZkNvRd0pyFdGpZNBErIwaryKQXqnkzg6pYaht6vfri8sabtqRP~sSEjMBvdMYBKLUfIvN2C3le4qnIn6rduzsdt5G71rAEebmEpsqb~JBYGWSy4x5fbkjzv-Qj817JsCT0dew_&Key-Pair-Id=APKAJLTNE6QMUY6HBC5A"
    
    # Parse the graph data from the URL
    edges, number_of_nodes = parse_graph_data(url)
    
    # Set the desired number of clusters
    k = 4
    
    # Find the maximum spacing for the clustering
    max_spacing = maximum_spacing_clustering(edges, number_of_nodes, k)
    print(max_spacing)

if __name__ == "__main__":
    main()
