from typing import List
import unittest

def quick_sort(array: List[int]):
    validate(array)
    if len(array) in (0, 1):
        return
    place_pivot(array, 0, len(array)-1)
    return

def validate(array: List[int]):
    pass

def place_pivot(array: List[int], start: int, end: int):
    print(array, start, end)
    if start >= end:
        return
    pivot_num = array[end]
    left_p = start
    right_p = end - 1
    while left_p < right_p:
        if array[left_p] <= pivot_num:
            left_p += 1
        elif array[right_p] > pivot_num:
            right_p -= 1
        else:
            array[left_p], array[right_p] = \
                array[right_p], array[left_p]
            left_p += 1
            right_p -= 1
    if left_p != right_p or array[left_p] > pivot_num:      
        array[left_p], array[end] = array[end], array[left_p]
        pivot = left_p
    else:
        pivot = end

    place_pivot(array, start, pivot-1)
    place_pivot(array, pivot+1, end)
    print("end")
    
    return

"""
testcase1:
array = [15, 10, 20, 5]
                     *
[5, 10, 20, 15]

2, 1,  3, 7, 5
       r  l

4, 2, 1, 7, 5
         lr

2, 7, 6, 8, 5
r  l

2, 6, 7, 8, 5
   lr

l == r
"""

class TestQuickSort(unittest.TestCase):
    
    def test_quick_sort(self):
        array = [15, 10, 20, 5]
        quick_sort(array)
        self.assertEqual([5, 10, 15, 20], array)
    
if __name__ == '__main__':
    unittest.main()