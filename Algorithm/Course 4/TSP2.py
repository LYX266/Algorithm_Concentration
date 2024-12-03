# TSP with Nearest Neighbor Heuristic

import math
import requests
from typing import List, Tuple

# Function to calculate squared Euclidean distance
def squared_distance(city1: Tuple[float, float], city2: Tuple[float, float]) -> float:
    return (city1[0] - city2[0]) ** 2 + (city1[1] - city2[1]) ** 2

# Function to calculate Euclidean distance
def euclidean_distance(city1: Tuple[float, float], city2: Tuple[float, float]) -> float:
    return math.sqrt((city1[0] - city2[0]) ** 2 + (city1[1] - city2[1]) ** 2)

# Function to implement the Nearest Neighbor Heuristic
def nearest_neighbor_tsp(cities: List[Tuple[float, float]]) -> int:
    num_cities = len(cities)
    visited = [False] * num_cities
    current_city = 0  
    visited[current_city] = True
    total_distance = 0

    for _ in range(num_cities - 1):
        nearest_city = -1
        min_distance = float('inf')

        # Find the nearest unvisited city
        for i in range(num_cities):
            if not visited[i]:
                dist = squared_distance(cities[current_city], cities[i])
                if dist < min_distance or (dist == min_distance and i < nearest_city):
                    min_distance = dist
                    nearest_city = i

        # Move to the nearest city
        total_distance += math.sqrt(min_distance)  # Use actual Euclidean distance here
        visited[nearest_city] = True
        current_city = nearest_city

    # Return to the starting city
    total_distance += euclidean_distance(cities[current_city], cities[0])

    # Return the total cost rounded down to the nearest integer
    return math.floor(total_distance)

def main():
    url = "https://d3c33hcgiwev3.cloudfront.net/_ae5a820392a02042f87e3b437876cf19_nn.txt?Expires=1733356800&Signature=KztW3PZu8j5N7Ja~wHvUnYGhGpkVBNbPup40xmqUI3gJHEg111Qwf-BrEpHqtM-4Moo~Le7dQIlOHF7Q1j79iM4YFZkp1M4Tuq~wx425Vc9cQTpuZzdRxUUeZSScqJ1kQaDYNspbN3blfUw0zjhhgj2CX51T7gemjmO1ZfZaXfI_&Key-Pair-Id=APKAJLTNE6QMUY6HBC5A"
    
    response = requests.get(url)
    data = response.text.strip().split('\n')

    print("First few lines of data:", data[:5])

    num_cities = int(data[0].strip())  # First line is the number of cities
    cities = []

    # Process each line and filter out invalid data
    for line in data[1:]:
        values = line.strip().split()
        if len(values) == 3:  # Ensure the line has exactly three values (index, x, y)
            try:
                # Skip the index and parse x and y as floats
                x, y = map(float, values[1:])  
                cities.append((x, y))
            except ValueError:
                continue  # Skip the line if it contains invalid numbers

    # Debug: Print the number of parsed cities
    print("Number of parsed cities:", len(cities))

    # Validate that the number of parsed cities matches the first line
    if len(cities) != num_cities:
        raise ValueError(f"Expected {num_cities} cities, but parsed {len(cities)}.")

    # Compute the TSP tour cost using the nearest neighbor heuristic
    total_cost = nearest_neighbor_tsp(cities)

    # Output the total cost
    print(total_cost)

if __name__ == "__main__":
    main()
