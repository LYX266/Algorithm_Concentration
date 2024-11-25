def optimal_bst(keys, freq):
    n = len(keys)
    
    # Initialize the cost and weight tables
    C = [[0] * n for _ in range(n)]
    W = [[0] * n for _ in range(n)]
    
    # Fill the weight table W[i][j]
    for i in range(n):
        W[i][i] = freq[i]
        for j in range(i + 1, n):
            W[i][j] = W[i][j - 1] + freq[j]
    
    # Fill the cost table C[i][j] using the recurrence relation
    for length in range(1, n + 1):  # length of the range
        for i in range(n - length + 1):
            j = i + length - 1
            # Initialize C[i][j] to a large value
            C[i][j] = float('inf')
            
            # Try making each key k_r (where i <= r <= j) the root
            for r in range(i, j + 1):
                # Cost of left and right subtrees
                cost_left = C[i][r - 1] if r > i else 0
                cost_right = C[r + 1][j] if r < j else 0
                # Calculate cost with k_r as the root
                cost = cost_left + cost_right + W[i][j]
                
                # Update the minimum cost for C[i][j]
                C[i][j] = min(C[i][j], cost)
    
    # The answer is the minimum cost to construct an OBST for keys 1 to n
    return C[0][n - 1]

# Given data
keys = [1, 2, 3, 4, 5, 6, 7]
freq = [0.2, 0.05, 0.17, 0.1, 0.2, 0.03, 0.25]

# Calculate minimum possible average search time
min_avg_search_time = optimal_bst(keys, freq)
print("Minimum possible average search time:", min_avg_search_time)
