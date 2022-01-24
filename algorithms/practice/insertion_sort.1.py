from typing import List
import unittest

def insertion_sort(array: List[int]):
    validate(array)
    if len(array) in (0, 1):
        return
    for i in range(1, len(array)):
        num = array[i]
        j = i - 1
        while j >= 0 and array[j] > num:
            array[j+1] = array[j]
            j -= 1
        array[j+1] = num
    return

def validate(array: List[int]):
    pass

"""
testcase1:
array = [5, 10, 15, 20]
i = 3
num = 20
j = 2


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
