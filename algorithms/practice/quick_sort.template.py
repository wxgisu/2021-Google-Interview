from typing import List
import unittest

def quick_sort(array: List[int]):
    pass

def validate(array: List[int]):
    pass

def place_pivot(array: List[int], start: int, end: int):
    pass

"""
testcase1:
array = [15, 10, 20, 5]

"""

class TestQuickSort(unittest.TestCase):
    
    def test_quick_sort(self):
        array = [15, 10, 20, 5]
        quick_sort(array)
        self.assertEqual([5, 10, 15, 20], array)
    
if __name__ == '__main__':
    unittest.main()