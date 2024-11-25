import requests
from functools import lru_cache
import sys
sys.setrecursionlimit(10000)  # Increase the recursion limit


# Fetch the input data from the URL
def fetch_data_from_url(url):
    response = requests.get(url)
    response.raise_for_status()  # Ensure the request was successful
    data = response.text.strip().splitlines()
    return data

# Knapsack function using top-down recursive approach with memoization
def knapsack_recursive(knapsack_size, items):
    # Memoization dictionary
    memo = {}

    # Recursive function with memoization
    def knapsack(i, remaining_capacity):
        # Base case: no items left or no capacity left
        if i >= len(items) or remaining_capacity <= 0:
            return 0

        # Check if result is already computed
        if (i, remaining_capacity) in memo:
            return memo[(i, remaining_capacity)]

        value, weight = items[i]

        # Option 1: Exclude the item
        exclude_item = knapsack(i + 1, remaining_capacity)

        # Option 2: Include the item (only if it fits in the knapsack)
        include_item = 0
        if weight <= remaining_capacity:
            include_item = value + knapsack(i + 1, remaining_capacity - weight)

        # Take the maximum of including or excluding the item
        result = max(exclude_item, include_item)

        # Store the result in memo
        memo[(i, remaining_capacity)] = result
        return result

    # Start the recursive knapsack function
    return knapsack(0, knapsack_size)

# URL for the input file
url = "https://d3c33hcgiwev3.cloudfront.net/_6dfda29c18c77fd14511ba8964c2e265_knapsack1.txt?Expires=1731024000&Signature=TSjMxWx3e4iMrmst-Uh1UdwywA0yvtUjTCq6TrPq7Z-b2rswYD4-gt7PT-~JAPmIG8uG59yoNyCalVSmZuSzItAmT8jf9iBDhWHYUuN1mJ05GPrltBSvbHL15LxQbZt5qNv1ocZtXJoir0q5tP5A3L1ItqCrTF0fJf67MuUSo1Y_&Key-Pair-Id=APKAJLTNE6QMUY6HBC5A"

# Fetch and parse data from the URL
data = fetch_data_from_url(url)

# Parse the first line for knapsack size and number of items
knapsack_size, number_of_items = map(int, data[0].strip().split())

# Parse each item's value and weight
items = []
for line in data[1:]:
    value, weight = map(int, line.strip().split())
    items.append((value, weight))

# Call the recursive knapsack function and print the result
optimal_value = knapsack_recursive(knapsack_size, items)
print("Optimal solution value:", optimal_value)
