from typing import List
import unittest

def insertion_sort(array: List[int]):
    pass

def validate(array: List[int]):
    pass

"""
testcase1:
array = [5, 10, 15, 20]
"""

class TestInsertionSort(unittest.TestCase):
    def test_insertion_sort1(self):
        array = [1, 3, 2, 5, 4, 9]    
        expected = [1, 2, 3, 4, 5, 9]
        insertion_sort(array)
        self.assertEqual(expected, array)
    
    def test_insertion_sort2(self):
        array = [3]
        insertion_sort(array)
        self.assertEqual([3], array)
    
    def test_insertion_sort3(self):
        array = []
        insertion_sort(array)
        self.assertEqual([], array)

if __name__ == '__main__':
    unittest.main()
