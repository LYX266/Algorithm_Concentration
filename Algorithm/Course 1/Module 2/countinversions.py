# Count inversions using divide and conquer

def count_inversions(arr):
    if len(arr) <= 1: # base case
        return arr, 0
    
    # divide and count inversions for left and right type
    mid = len(arr) // 2
    left, inv_left = count_inversions(arr[:mid])
    right, inv_right = count_inversions(arr[mid:])
    
    # merge and count split inversions
    merged, inv_merge = merge_and_count(left, right)
    
    return merged, inv_left + inv_right + inv_merge

# merge and count subroutine for split inversions
def merge_and_count(left, right):
    merged = []
    i, j = 0, 0
    inv_count = 0
    
    # merge the two arrays in sorted order
    while i < len(left) and j < len(right):
        if left[i] <= right[j]:
            merged.append(left[i])
            i += 1
        else:
            merged.append(right[j])
            j += 1
            # number of inversions is the number of elements remaining in the left array
            inv_count += len(left) - i
    
    # add remaining elements from left and right
    merged.extend(left[i:])
    merged.extend(right[j:])
    
    return merged, inv_count

# read array from url
import requests
from countinversions import count_inversions

def read_array_from_url(url):
    response = requests.get(url)
    response.raise_for_status()  # Raise an error for bad status codes
    array = response.text.strip().split('\n')
    array = list(map(int, array))
    return array

if __name__ == "__main__":
    url = 'https://d3c33hcgiwev3.cloudfront.net/_bcb5c6658381416d19b01bfc1d3993b5_IntegerArray.txt?Expires=1727308800&Signature=OX5iUdPskQaTKS78V-J2wOLX3Qy01hprnPo2AIFrTH-2FMH6lNUUWBf0dlBglgS55bv-LOQ4LcwczGG4VBS62sSWoHBD2uiVhKxengY14Kksq~CsHwnI6URhZIvip1H~8OBSPGK851FqoBnbxvTm0za5uDpZm5NfIgzkxVB2iqo_&Key-Pair-Id=APKAJLTNE6QMUY6HBC5A'
    array = read_array_from_url(url)
    _, inversion_count = count_inversions(array)
    print(f"Number of inversions: {inversion_count}")


