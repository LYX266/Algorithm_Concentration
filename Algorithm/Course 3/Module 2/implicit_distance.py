import requests
from collections import defaultdict

class UnionFind:
    def __init__(self, size):
        self.parent = list(range(size))
        self.rank = [1] * size
        self.count = size  # Keeps track of the number of clusters
    
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

    def get_count(self):
        return self.count

def parse_data(url):
    response = requests.get(url)
    response.raise_for_status()
    lines = response.text.strip().split('\n')
    
    # First line contains number of nodes and number of bits
    number_of_nodes, number_of_bits = map(int, lines[0].strip().split())
    
    # Parse each node's label as an integer
    labels = []
    node_map = {}  # Maps label to node index
    index = 0
    
    for line in lines[1:]:
        bits = line.strip().replace(" ", "")
        label = int(bits, 2)  # Convert bitstring to integer
        if label not in node_map:  # Avoid duplicates
            labels.append(label)
            node_map[label] = index
            index += 1

    return labels, node_map, number_of_bits

def generate_neighbors(label, num_bits):
    """Generate all neighbors of 'label' with Hamming distance of 1 or 2."""
    neighbors = []
    for i in range(num_bits):
        # Flip one bit to get a neighbor at Hamming distance 1
        neighbor1 = label ^ (1 << i)
        neighbors.append(neighbor1)
        # Flip two bits to get neighbors at Hamming distance 2
        for j in range(i + 1, num_bits):
            neighbor2 = label ^ (1 << i) ^ (1 << j)
            neighbors.append(neighbor2)
    return neighbors

def clustering_with_spacing(labels, node_map, num_bits):
    n = len(labels)
    uf = UnionFind(n)
    
    # For each label, attempt to union with all labels at Hamming distance <= 2
    for label in labels:
        node = node_map[label]
        for neighbor in generate_neighbors(label, num_bits):
            if neighbor in node_map:
                neighbor_node = node_map[neighbor]
                uf.union(node, neighbor_node)
    
    return uf.get_count()

def main():
    url = "https://d3c33hcgiwev3.cloudfront.net/_fe8d0202cd20a808db6a4d5d06be62f4_clustering_big.txt?Expires=1730678400&Signature=fsY79fG4ihBdiGiDM4TlT3Bjiw0iHDQShfQd~GEJB31bJ0iMjojI62N~r8Nm067EBw2fq7X7vyyX1OP2VUm5oBpVj~OxUB1GkPlmlVzFt1eww5g96NLsoYNwgKaDWCQX~aeDrv81udrkQjj3wPUD~p3pvaigqruWWj-NMdGjpj8_&Key-Pair-Id=APKAJLTNE6QMUY6HBC5A"
    
    # Parse data
    labels, node_map, num_bits = parse_data(url)
    
    # Perform clustering with the condition that spacing is at least 3
    num_clusters = clustering_with_spacing(labels, node_map, num_bits)
    print(num_clusters)

if __name__ == "__main__":
    main()
