"""two sum variant"""

import requests

# Function to download numbers from the URL and store them in a set
def download_numbers(url):
    response = requests.get(url)
    response.raise_for_status()  # Ensure the request was successful
    # Parse each line as an integer and store in a set for quick lookups
    numbers = set(map(int, response.text.strip().splitlines()))
    return numbers

# Optimized two-sum variant using a hash table
def two_sum_variant(numbers, target_range):
    valid_targets = set()  # Set to store unique valid targets

    # Iterate over each number in `numbers`
    for x in numbers:
        # Check for each possible target value t in the range
        for t in range(target_range[0], target_range[1] + 1):
            y = t - x
            # Check if y is in numbers and y is distinct from x
            if y in numbers and y != x:
                valid_targets.add(t)
                # No need to break, as we want to find all valid targets

    return len(valid_targets)

# Main function to handle downloading, processing, and outputting the result
def main():
    # URL of the input file
    url = "https://d3c33hcgiwev3.cloudfront.net/_6ec67df2804ff4b58ab21c12edcb21f8_algo1-programming_prob-2sum.txt?Expires=1730332800&Signature=XG5zTKBt5vC~sFModXc6ALHNcW02~z8Oh5Tu1efBGk00CcK1sy4p0V6MIBznozKyHwipGf~nCZm9LpMYfLhVGlFVk91Inyx0P33eDEYMgW1VQcvfdvdIaVEtccl9pniztlavqXPVPypD~dmrwqDEyd0WrdCGvwqCnAgz9CmgLv8_&Key-Pair-Id=APKAJLTNE6QMUY6HBC5A"  
    
    # Download the numbers from the URL
    numbers = download_numbers(url)

    # Define the target range as [-10000, 10000]
    target_range = (-10000, 10000)

    # Run the two-sum variant algorithm and get the result
    result = two_sum_variant(numbers, target_range)
    
    # Print the result
    print(result)

if __name__ == "__main__":
    main()
