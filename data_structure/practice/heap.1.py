from typing import List, Optional
import unittest
import copy

class MaxHeap:
    def __init__(self, array: List[int] = []):
        self.heap = copy.copy(array)
        self.size = len(self.heap)
        self.validate()
        self.build_heap()

    def validate(self):
        pass

    def build_heap(self):
        if self.size == 0:
            return
        last_parent_index = self.size // 2 - 1
        for i in range(last_parent_index, -1, -1):
            self._fix_parent(i)
    
    def get_heap(self):
        return self.heap[:self.size]
    
    def heapify(self, index: int) -> int:
        while index != None:
            new_index = self._fix_parent(index)
            if new_index == index:
                return index
            index = new_index
        return index

    def peek(self) -> Optional[int]:
        return self.heap[0] if self.size > 0 else None
    
    def push(self, value: int) -> int:
        index = self.size
        if len(self.heap) == self.size:
            self.heap.append(value)
        else:
            self.heap[index] = value
        self.size += 1
        index = self._bubble_up(index)
        return index
    
    def pop(self) -> Optional[int]:
        if self.size == 0:
            return None
        value = self.heap[0]
        self.heap[0] = self.heap[self.size - 1]
        self.size -= 1
        self.heapify(0)
        return value
    
    def _fix_parent(self, parent_index: int):
        left_index = self._get_left_index(parent_index)    
        right_index = self._get_right_index(parent_index)
        
        if left_index == right_index == None:
            return None
        if left_index == None:
            max_index = right_index
        elif right_index == None:
            max_index = left_index
        elif self.heap[left_index] >= self.heap[right_index]:
            max_index = left_index
        else:
            max_index = right_index
        
        if self.heap[parent_index] < self.heap[max_index]:
            self.heap[parent_index], self.heap[max_index] = \
                self.heap[max_index], self.heap[parent_index]
            return max_index
        return parent_index

    def _get_left_index(self, parent_index: int) -> int:
        left_index = 2 * parent_index + 1
        if left_index >= self.size:
            return None
        return left_index
    
    def _get_right_index(self, parent_index: int) -> int:
        right_index = 2 * parent_index + 2
        if right_index >= self.size + 1:
            return None
        return right_index
    
    def _get_parent_index(self, index: int) -> int:
        if index == 0:
            return None
        return (index - 1) // 2

    def _bubble_up(self, index: int) -> int:
        parent_index = self._get_parent_index(index)

        while parent_index != None and self.heap[index] > self.heap[parent_index]:
            self.heap[index], self.heap[parent_index] = \
                self.heap[parent_index], self.heap[index]
            index = parent_index
            parent_index = self._get_parent_index(index)

        return index
    
"""
        9
       /  \
      3*  10
     /  \
    2    5
        ↓
    
      9*
     /  \
    5    10
   / \
  2   3
          ↓
    
      10
     /  \
    5    9
   / \
  2   3


      5
     /  \
    3    1
   / 
  2   
"""

class TestMaxHeap(unittest.TestCase):
    
    def test_build_heap(self):
        array = [9, 3, 10, 2, 5]
        heap = MaxHeap(array)
        self.assertEqual([10, 5, 9, 2, 3], heap.heap)
    
    def test_heapify(self):
        array = [10, 9, 5, 2, 3]
        heap = MaxHeap(array)
        heap.heap[0] = 1
        heap.heapify(0)
        self.assertEqual([9, 3, 5, 2, 1], heap.heap)

    def test_peek(self):
        array = [9, 3, 10, 2, 5]
        heap = MaxHeap(array)
        self.assertEqual(10, heap.peek())
    
    def test_push(self):
        array = [9, 3, 5, 2, 1]
        heap = MaxHeap(array)
        print(heap.heap)
        heap.push(12)
        self.assertEqual([12, 3, 9, 2, 1, 5], heap.heap)
    
    def test_pop(self):
        array = [9, 3, 5, 2, 1]
        heap = MaxHeap(array)
        heap.pop()
        self.assertEqual([5, 3, 1, 2], heap.get_heap())

if __name__ == '__main__':
    unittest.main()