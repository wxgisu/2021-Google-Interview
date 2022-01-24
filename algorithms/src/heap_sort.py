import os
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent.parent
sys.path.append(str(ROOT))
from data_structure.src.heap import MaxHeap
from typing import List
import unittest

def heap_sort(array: List[List[int]]):
    heap = MaxHeap(array)
    result = []
    while heap.size > 0:
        result.append(heap.pop())
    result.reverse()
    return result





class TestHeapSort(unittest.TestCase):
    
    def test_heap_sort(self):
        array = [5, 2, 6, 1, 9, 100, 3, 7]
        expected = [1, 2, 3, 5, 6, 7, 9, 100]
        actual = heap_sort(array)
        self.assertEqual(expected, actual)

if __name__ == '__main__':
    unittest.main()