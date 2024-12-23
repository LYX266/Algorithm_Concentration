def quicksort(arr):
    comparisons = [0]  # Use a list to pass by reference

    def median_of_three(low, high):
        mid = low + (high - low) // 2
        a, b, c = arr[low], arr[mid], arr[high]
        if a > b:
            if a < c:
                return low
            elif b > c:
                return mid
            else:
                return high
        else:
            if a > c:
                return low
            elif b < c:
                return mid
            else:
                return high

    def partition(low, high):
        pivot_index = median_of_three(low, high)
        arr[low], arr[pivot_index] = arr[pivot_index], arr[low]  # Swap pivot to the start so the rest goes as the same as 1
        pivot = arr[low]
        i = low
        for j in range(low + 1, high + 1):
            if arr[j] < pivot:
                i += 1
                arr[i], arr[j] = arr[j], arr[i]
        arr[i], arr[low] = arr[low], arr[i]
        return i

    def quicksort_recursive(low, high):
        if low < high:
            comparisons[0] += (high - low)  # Add the number of comparisons for this partition
            pi = partition(low, high)
            quicksort_recursive(low, pi - 1)
            quicksort_recursive(pi + 1, high)

    quicksort_recursive(0, len(arr) - 1)
    return comparisons[0]

import requests
def read_array_from_url(url):
    response = requests.get(url)
    response.raise_for_status()  # Raise an error for bad status codes
    array = response.text.strip().split('\n')
    array = list(map(int, array))
    return array

if __name__ == "__main__":
    url = 'https://d3c33hcgiwev3.cloudfront.net/_32387ba40b36359a38625cbb397eee65_QuickSort.txt?Expires=1727740800&Signature=ZQuxkQcZ~rE8-I0jJQiL1CK4gwtrE3E9L4NR9bDgyjKtlqEndcsqpEa9SdCWr-xMlheMGBTz8-LKMjYQ82AcYlZPKn4OtBfNzkeoOs4y-S8myrbvoJ03FXVhtSPQitPmzIyE2gZC1nOfynNo2qAgsDHr7nsWSxFPY~pNVwcrbrE_&Key-Pair-Id=APKAJLTNE6QMUY6HBC5A'
    array = read_array_from_url(url)
    comparisons = quicksort(array)
    print(f"Number of comparisons: {comparisons}")
