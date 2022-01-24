from typing import List
import unittest

def merge_sort(array: List[int], start: int, end: int):
    pass

def validate(array: List[int]):
    pass

def merge(array: List[int], start: int, mid: int, end: int):
    pass

"""
testcase1:
array = [5, 1, 2]
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