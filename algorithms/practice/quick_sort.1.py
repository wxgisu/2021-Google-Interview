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
    if start >= end:
        return
    pivot = array[end]
    left_p = start
    right_p = end - 1
    while left_p <= right_p:
        if array[left_p] <= pivot:
            left_p += 1
        elif array[right_p] > pivot:
            right_p -= 1
        else:
            array[left_p], array[right_p] = \
                array[right_p], array[left_p]
            left_p += 1
            right_p -= 1
    array[left_p], array[end] = array[end], array[left_p]
    place_pivot(array, start, left_p-1)
    place_pivot(array, left_p+1, end)
    pass

"""
testcase1:
array = [15, 10, 20, 5]
place_pivot[15, 10, 20, 5], 0, 3)
    array = [5, 10, 20, 15]
             <        
         >
    place_pivot([5, 10, 20, 15], 0, -1)
    place_pivot([5, 10, 20, 15], 1, 3)
        array = [5, 10, 15, 20]
                        <
                    >
        place_pivot([5, 10, 15, 20], 1, 1)
        place_pivot([5, 10, 15, 20], 3, 3)
        return
"""

class TestQuickSort(unittest.TestCase):
    
    def test_quick_sort(self):
        array = [15, 10, 20, 5]
        quick_sort(array)
        self.assertEqual([5, 10, 15, 20], array)
    
if __name__ == '__main__':
    unittest.main()