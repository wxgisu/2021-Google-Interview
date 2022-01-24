from typing import List
import unittest

def merge_sort(array: List[int], start: int, end: int):
    if start == end:
        return
    mid = (start + end) // 2
    merge_sort(array, start, mid)
    merge_sort(array, mid+1, end)
    merge(array, start, mid, end)
    return

def validate(array: List[int]):
    pass

def merge(array: List[int], start: int, mid: int, end: int):
    left = array[start: mid+1]
    right = array[mid+1: end+1]
    left_pointer = right_pointer = 0
    pointer = start

    while left_pointer < len(left) or right_pointer < len(right):
        left_value = left[left_pointer] if left_pointer < len(left) else float('inf')
        right_value = right[right_pointer] if right_pointer < len(right) else float('inf')
        if left_value < right_value:
            array[pointer] = left_value
            left_pointer += 1
        else:
            array[pointer] = right_value
            right_pointer +=1
        pointer += 1

    return

"""
testcase1:
array = [5, 1, 2]
start = 0
end = 2
mid = 1
merge_sort([5, 1, 2], 0, 2)

# left
merge_sort([5, 1, 2], 0, 1)
merge_sort([5, 1, 2], 0, 0)
merge_sort([5, 1, 2], 1, 1)
merge([5, 1, 2], 0, 0, 1)
left [5]
right [1]
array = [1, 5, 2]

# right
merge_sort([5, 1, 2], 2, 2)
merge([1, 5, 2], 0, 1, 2)
left [1, 5]
right [2]

[1, 2, 5]
"""

class TestMergeSort(unittest.TestCase):

    def test_merge_sort(self):
        array = [5, 1, 2]
        merge_sort(array, 0, 2)
        self.assertEqual([1, 2, 5], array)

    def test_merge_sort(self):
        array = [100, 3, 49, 50, -12]
        merge_sort(array, 0, len(array)-1)
        self.assertEqual([-12, 3, 49, 50, 100], array)
    
if __name__ == '__main__':
    unittest.main()