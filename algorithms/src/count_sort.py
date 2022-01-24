from typing import List
import unittest

def count_sort(array: List[int]) -> List[int]:
    validate(array) 
    if len(array) == 0:
        return []
    
    result = [0] * len(array)
    count = [0] * (max(array) + 1)
    
    for num in array:
        count[num] += 1

    for i in range(len(count) - 1):
        count[i+1] += count[i]

    for i in range(len(array)-1, -1, -1):
        num = array[i]
        index = count[num] - 1
        result[index] = num
        count[num] -= 1

    return result

"""
testcase1: 
array = [2, 4, 2, 1]
count = [0, 0, 2, 3, 3]
num = 2
index = 1
result = [1, 2, 2, 4]
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

if __name__ == '__main__':
    unittest.main()