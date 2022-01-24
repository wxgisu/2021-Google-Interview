from typing import List
import unittest

def count_sort(array: List[int]) -> List[int]:
    pass

"""
testcase1: 
array = [2, 4, 2, 1]
"""

def validate(array: List[int]):
    if min(array) < 0:
        raise ValueError("This version of count sort only support positive integers")
    pass

class TestCountSort(unittest.TestCase):
    
    def test_count_sort(self):
        array = [2, 4, 2, 1]
        expected = [1, 2, 2, 4]
        actual = count_sort(array)
        self.assertEqual(expected, actual)
    
    def test_count_sort2(self):
        array = [3, 2, 7, 1, 9, 0, 100, 100, 101]
        expected = [0, 1, 2, 3, 7, 9, 100, 100, 101]
        actual = count_sort(array)
        self.assertEqual(expected, actual)
    
    def test_count_sort_raise_exception_on_negative_input(self):
        array = [2, -4, 2, 1]
        self.assertRaises(ValueError, count_sort, array)

if __name__ == '__main__':
    unittest.main()