import requests
import heapq

class Node:
    def __init__(self, weight, left=None, right=None):
        self.weight = weight
        self.left = left
        self.right = right

    # Define comparison operators for priority queue to work
    def __lt__(self, other):
        return self.weight < other.weight

def download_data(url):
    response = requests.get(url)
    data = response.text.strip().splitlines()
    return [int(line) for line in data[1:]]  # Skip the first line (number of symbols)

def huffman_tree(weights):
    # Step 1: Initialize the priority queue with all weights as leaf nodes
    heap = [Node(weight=w) for w in weights]
    heapq.heapify(heap)

    # Step 2: Build the Huffman Tree
    while len(heap) > 1:
        # Pop the two smallest nodes
        left = heapq.heappop(heap)
        right = heapq.heappop(heap)

        # Combine them into a new node
        merged = Node(left.weight + right.weight, left, right)
        
        # Push the new node back into the priority queue
        heapq.heappush(heap, merged)

    # The remaining node is the root of the Huffman tree
    return heap[0]

def calculate_codeword_lengths(root):
    # Use DFS to determine the depth of each leaf
    def dfs(node, depth):
        if node.left is None and node.right is None:
            # Leaf node
            lengths.append(depth)
            return
        if node.left:
            dfs(node.left, depth + 1)
        if node.right:
            dfs(node.right, depth + 1)
    
    lengths = []
    dfs(root, 0)
    return min(lengths), max(lengths)

def main(url):
    # Step 1: Download and parse data
    weights = download_data(url)
    
    # Step 2: Construct the Huffman Tree
    root = huffman_tree(weights)
    
    # Step 3: Calculate the minimum and maximum codeword lengths
    min_length, max_length = calculate_codeword_lengths(root)
    
    print(f"Minimum codeword length: {min_length}")
    print(f"Maximum codeword length: {max_length}")

# Replace 'your_url_here' with the actual URL containing the data
url = "https://d3c33hcgiwev3.cloudfront.net/_eed1bd08e2fa58bbe94b24c06a20dcdb_huffman.txt?Expires=1730851200&Signature=jWxTLMPGqRlbFo9IUE9auLupmPRfe979dK3zcuUBt271akN~9bA3RcRQ-Yx8S57xa01XcWBlJM2BX8ezrcvZohEU7GlQPhQiQkCrHB7A-G0D0IxmVluHms~Zhl1vn710J0sBsc8qrIjCcVNJjuN3Z1YZ-F9hMm1FkJ1DM7AVLA0_&Key-Pair-Id=APKAJLTNE6QMUY6HBC5A"
main(url)
