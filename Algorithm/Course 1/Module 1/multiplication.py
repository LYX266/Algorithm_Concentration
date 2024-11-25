# Multiplication algorithm

def karatsuba(x, y):
    # Base case for recursion: single-digit multiplication
    if x < 10 and y < 10:
        return x * y

    # Calculate the size of the numbers
    n = max(len(str(x)), len(str(y)))
    half = n // 2

    # Split the digit sequences in the middle
    high1, low1 = divmod(x, 10**half)
    high2, low2 = divmod(y, 10**half)

    # 3 recursive calls to Karatsuba
    z0 = karatsuba(low1, low2)
    z1 = karatsuba((low1 + high1), (low2 + high2))
    z2 = karatsuba(high1, high2)

    # Combine the results
    return (z2 * 10**(2*half)) + ((z1 - z2 - z0) * 10**half) + z0

# Ask the user to input two integers
num1 = int(input("Enter the first integer: "))
num2 = int(input("Enter the second integer: "))

# Print the input integers
print(f"The first integer is: {num1}")
print(f"The second integer is: {num2}")

# Perform Karatsuba multiplication
result = karatsuba(num1, num2)
print(f"The product of {num1} and {num2} using Karatsuba algorithm is: {result}")

