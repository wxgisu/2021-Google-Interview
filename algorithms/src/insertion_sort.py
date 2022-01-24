from typing import List
import unittest

def insertion_sort(array: List[int]):
    n = len(array)
    if n in (0, 1):
        return
    
    for i in range(1, n):
        value = array[i]
        j = i - 1
        while j >= 0 and array[j] > value:
            array[j + 1] = array[j]
            j -= 1
        array[j + 1] = value

    return

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
