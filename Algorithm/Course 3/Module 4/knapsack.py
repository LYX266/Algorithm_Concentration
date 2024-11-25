import requests

def knapsack(knapsack_size, items):
    # DP array to store maximum values for each capacity up to knapsack_size
    dp = [0] * (knapsack_size + 1)
    
    # Dynamic programming to solve knapsack problem
    for value, weight in items:
        # Traverse dp array backwards to avoid reuse of the same item
        for w in range(knapsack_size, weight - 1, -1):
            dp[w] = max(dp[w], dp[w - weight] + value)

    # The maximum value for the full knapsack capacity
    return dp[knapsack_size]

# Function to fetch data from a URL
def fetch_data_from_url(url):
    response = requests.get(url)
    response.raise_for_status()  # Check if the request was successful
    data = response.text.strip().splitlines()
    return data

# URL of the knapsack input file
url = "https://d3c33hcgiwev3.cloudfront.net/_6dfda29c18c77fd14511ba8964c2e265_knapsack_big.txt?Expires=1731024000&Signature=jAxOGurtR4wfNRGBoBZnmXojOXB2kGqbE8vAJDmUnqEoT3RL-QIB3EWv4CynEyGTi5iuQMToQsgava0rJHwIuEcDEzqTKhVa1Quua5wizTpPUC2oW56RjmaZthRfjT8fbfUDCBafe5S6ohK0Gn3Bewao8BIgiPwG~5KXC5nBFag_&Key-Pair-Id=APKAJLTNE6QMUY6HBC5A" 

# Fetch and parse data from the URL
data = fetch_data_from_url(url)

# Parse the first line for knapsack size and number of items
knapsack_size, number_of_items = map(int, data[0].strip().split())

# Parse each item's value and weight
items = []
for line in data[1:]:
    value, weight = map(int, line.strip().split())
    items.append((value, weight))

# Call the knapsack function and print the result
optimal_value = knapsack(knapsack_size, items)
print("Optimal solution value:", optimal_value)
