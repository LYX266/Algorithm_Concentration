import math
import requests
from functools import lru_cache

def euclidean_distance(point1, point2):
    """
    Calculate the Euclidean distance between two points.
    """
    return math.sqrt((point1[0] - point2[0]) ** 2 + (point1[1] - point2[1]) ** 2)

def tsp_min_cost(cities):
    """
    Solve the Traveling Salesman Problem using Dynamic Programming with bitmasking.
    Args:
    - cities (list of tuples): A list of (x, y) coordinates for the cities.

    Returns:
    - Minimum cost of a complete TSP tour rounded down to the nearest integer.
    """
    n = len(cities)
    
    # Precompute distances between every pair of cities
    dist = [[0] * n for _ in range(n)]
    for i in range(n):
        for j in range(n):
            dist[i][j] = euclidean_distance(cities[i], cities[j])
    
    # Dynamic programming cache
    # dp[mask][i] will hold the minimum cost to visit the set of cities represented by `mask`, ending at city `i`.
    @lru_cache(None)
    def dp(mask, i):
        """
        Recursive function to compute the minimum cost of visiting cities in `mask`, ending at city `i`.
        Args:
        - mask (int): A bitmask representing the set of cities visited.
        - i (int): The current city being considered as the endpoint.

        Returns:
        - Minimum cost of the tour ending at city `i` for the given mask.
        """
        # Base case: if mask only includes city 0, the cost is 0 (we start at city 0)
        if mask == 1 << i and i == 0:
            return 0
        
        # Otherwise, calculate the minimum cost of reaching city `i` from other cities
        min_cost = float('inf')
        for j in range(n):
            if mask & (1 << j) and j != i:  # Check if city `j` is in the mask and is not `i`
                min_cost = min(min_cost, dp(mask ^ (1 << i), j) + dist[j][i])
        return min_cost

    # Start the DP by trying to end at any city (all cities must be visited)
    all_visited_mask = (1 << n) - 1  # Bitmask where all `n` cities are visited
    min_tour_cost = float('inf')
    
    for i in range(1, n):  # Ending at cities 1 through n-1 (we return to city 0 later)
        min_tour_cost = min(min_tour_cost, dp(all_visited_mask, i) + dist[i][0])
    
    return math.floor(min_tour_cost)

def read_input_from_url(url):
    """
    Fetch input data from a URL where the first line contains the number of cities,
    and each subsequent line contains the coordinates of a city.
    Args:
    - url (str): URL to fetch the input data from.

    Returns:
    - cities (list of tuples): A list of (x, y) coordinates for the cities.
    """
    response = requests.get(url)
    response.raise_for_status()  # Ensure the request was successful
    lines = response.text.strip().split("\n")
    n = int(lines[0].strip())  # First line: number of cities
    cities = []
    for line in lines[1:]:
        x, y = map(float, line.strip().split())
        cities.append((x, y))
    return cities

# Main execution
if __name__ == "__main__":
    # URL input
    url = 'https://d3c33hcgiwev3.cloudfront.net/_f702b2a7b43c0d64707f7ab1b4394754_tsp.txt?Expires=1731888000&Signature=LJi~OcWZsMmCmemnCNokkgonrIC5smVk~l5ERTTiuIIDQi5j1GfCJw73-mF-dACsk1D9glTt-VWB91RyT0Oduq2E7CgnnCrHbLH-rWI6oUeiaS7FlbqTPVCvGPdnHxgw7wL4wHEOmCwTIJp2YBT-B3JI63wrCSMC9ieYn-1TJ18_&Key-Pair-Id=APKAJLTNE6QMUY6HBC5A'
    cities = read_input_from_url(url)
    result = tsp_min_cost(cities)
    print(result)  # Output the result rounded down to the nearest integer
