import requests

def download_data(url):
    response = requests.get(url)
    data = response.text.strip().splitlines()
    return [int(line) for line in data[1:]]  # Skip the first line (number of vertices)

def compute_mwis(weights):
    n = len(weights)
    # DP array to store maximum weights
    A = [0] * (n + 1)
    
    # Base cases
    A[1] = weights[0]
    
    # Fill the DP table
    for i in range(2, n + 1):
        A[i] = max(A[i - 1], A[i - 2] + weights[i - 1])
    
    # Reconstruct the MWIS by backtracking
    mwis_set = set()
    i = n
    while i >= 1:
        if i == 1 or A[i - 1] < A[i - 2] + weights[i - 1]:
            mwis_set.add(i)  # Add vertex i to the MWIS
            i -= 2
        else:
            i -= 1
    
    return mwis_set

def main(url):
    # Step 1: Download and parse data
    weights = download_data(url)
    
    # Step 2: Compute the MWIS
    mwis_set = compute_mwis(weights)
    
    # Step 3: Check for specific vertices
    vertices_to_check = [1, 2, 3, 4, 17, 117, 517, 997]
    result = ''.join(['1' if v in mwis_set else '0' for v in vertices_to_check])
    
    print(f"8-bit result for specified vertices: {result}")

# Replace 'your_url_here' with the actual URL containing the data
url = "https://d3c33hcgiwev3.cloudfront.net/_790eb8b186eefb5b63d0bf38b5096873_mwis.txt?Expires=1730851200&Signature=ZmyDXCwTU9f~itsTo0BpYVeYa7bHWPJHytFFTOHkitvR9isnY6EL7EJFplObGsX8jhKrKlPLRAm1MaxVyHLfnhwtUbLi6RtXfIkD7Q0rTdZkHOupzRa7VqObHYosjkBPRKOgmlixKppVMsikKOa9-0h7aqD0zya2Q3kfhIn1PJ0_&Key-Pair-Id=APKAJLTNE6QMUY6HBC5A"
main(url)
