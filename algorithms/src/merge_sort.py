from typing import List

def merge_sort(array: List[int], start: int, end: int):
    if start >= end:
        return
    
    mid = (start + end) // 2
    merge_sort(array, start, mid)
    merge_sort(array, mid + 1, end)
    merge(array, start, mid, end)

    return 

def merge(array: List[int], start: int, mid: int, end: int):
    n_left = mid - start + 1
    n_right = end - mid

    left_array = [float('inf')] * (n_left + 1)
    right_array = [float('inf')] * (n_right + 1)
    
    left_array[0 : n_left] = array[start : start + n_left]
    right_array[0 : n_right] = array[mid + 1 : mid + 1 + n_right]

    left_pointer = 0
    right_pointer = 0

    for i in range(start, end+1):
        left = left_array[left_pointer]
        right = right_array[right_pointer]
        if left <= right:
            array[i] = left
            left_pointer += 1
        else:
            array[i] = right
            right_pointer += 1
    return

def merge_sort_v2(array: List[int], start: int, end: int) -> List[int]:
    # not in place version
    if start > end:
        return []
    if start == end:
        return array[start : start+1]
    
    mid = (start + end) // 2
    left_array = merge_sort_v2(array, start, mid)
    right_array = merge_sort_v2(array, mid+1, end)
    sorted_array = merge_v2(left_array, right_array) 
    
    return sorted_array

def merge_v2(array1: List[int], array2: List[int]) -> List[int]:
    pointer1 = pointer2 = 0
    sorted_array = []

    while pointer1 < len(array1) or pointer2 < len(array2):
        value1 = array1[pointer1] if pointer1 < len(array1) else float('inf')
        value2 = array2[pointer2] if pointer2 < len(array2) else float('inf')
        if value1 <= value2:
            sorted_array.append(value1)
            pointer1 += 1
        else:
            sorted_array.append(value2)
            pointer2 += 1
    
    return sorted_array
            
    
    


def main():
   test1 = [6, 3, 8, 1, 2]
   merge_sort(test1, 0, len(test1)-1)
   print(test1) 

   test2 = [6, 3, 8, 1, 2]
   res2 = merge_sort_v2(test2, 0, len(test2)-1)
   print(res2)

   
if __name__ == '__main__':
    main()