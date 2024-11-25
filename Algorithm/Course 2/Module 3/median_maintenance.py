"""median maintenance"""

import heapq
import requests

# Function to download the list of numbers from the URL
def download_numbers(url):
    response = requests.get(url)
    response.raise_for_status()  # Ensure the request was successful
    numbers = list(map(int, response.text.splitlines()))
    return numbers

# Median Maintenance Algorithm using two heaps
def median_maintenance(numbers):
    # Two heaps: max-heap for the lower half (low), min-heap for the upper half (high)
    low = []  # Max-heap (simulated with negative values)
    high = [] # Min-heap
    
    median_sum = 0
    
    for number in numbers:
        # Step 1: Insert the new number
        if len(low) == 0 or number <= -low[0]:
            heapq.heappush(low, -number)  # Push to max-heap (inverted value)
        else:
            heapq.heappush(high, number)  # Push to min-heap
        
        # Step 2: Balance the heaps
        if len(low) > len(high) + 1:
            heapq.heappush(high, -heapq.heappop(low))
        elif len(high) > len(low):
            heapq.heappush(low, -heapq.heappop(high))
        
        # Step 3: Calculate the current median
        if len(low) > len(high):
            median = -low[0]  # max of the low heap
        else:
            median = -low[0]  # still use max of the low heap (as defined in problem)
        
        # Step 4: Accumulate the median sum modulo 10000
        median_sum = (median_sum + median) % 10000
    
    # Return the sum of medians modulo 10000
    return median_sum

# Main function
def main():
    url = "https://d3c33hcgiwev3.cloudfront.net/_6ec67df2804ff4b58ab21c12edcb21f8_Median.txt?Expires=1730332800&Signature=SU-wfMFsylMM9USJw4SVrXCPDoKIGHmmZ8yJwDUgjU9DeccwYajlCeyDoJHPjJcTt30eeERgJZWXHVRCY5Fx7q8BKv~O1rvEUiCPV6V-F~uFAPmOHgESlahLFTkoIw-iLH~1kIn-7rJlJZqSDMCLhyQYXW9-nvwzcalN03ip5E0_&Key-Pair-Id=APKAJLTNE6QMUY6HBC5A"
    
    # Download the numbers
    numbers = download_numbers(url)
    
    # Run median maintenance algorithm and get result
    result = median_maintenance(numbers)
    
    # Output the result
    print(result)

if __name__ == "__main__":
    main()
