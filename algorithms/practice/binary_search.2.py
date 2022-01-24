from typing import List, Tuple
import unittest

"""
See behaviors for the three tempaltes here:
/Users/Xiaoguang/Study/knowledge-base/attachments/binary-search-templates.jpg

template_1 ends with invalid (start, end, mid) set, where start > end
template_2 ends with start == end == mid, the end nodes covers all possible index
tempalte_3 ends start + 1 == end, start == mid, the end nodes start, end covers all possible adjacent index pair, i.e (0,1) (1,2) ... (n-2, n-1)

template_1 only guarantee access to mid element in search space [start, end]
template_2 guaranttee access to mid element and its right neighbor in search space [start, end] 
template_3 guaranttee access to mid element and its left and right neighbors in search space [start, end]
"""
def binary_search_template_1(nums, target):
    """
    - Most basic and elementary form of Binary Search Search
    - Condition can be determined without comparing to the element's neighbors
      (or use specific elements around it) 
    - No post-processing required because at each step, you are checking to see
      if the element has been found. If you reach the end, then you know the
      element is not found
    
    @param nums: list of integer sorted in ascending order
    @param target: integer to find in nums
    @return: index of target in nums if found, -1 if not found
    """
    start = 0
    end = len(nums) - 1
    
    while start <= end:
        mid = (start + end) // 2
        if target == nums[mid]:
            return mid
        elif target < nums[mid]:
            end = mid - 1
        else:
            start = mid + 1
    
    return -1

def binary_search_template_2(nums, target):
    """
    - An advanced way to implement Binary Search.
    - Search Condition needs to access element's immediate right neighbor
    - Use element's right neighbor to determine if condition is met and decide
      whether to go left or right
    - Gurantees Search Space is at least 2 in size at each step
    - Post-processing required. Loop/Recursion ends when you have 1 element
      left. Need to assess if the remaining element meets the condition.

    @param nums: list of integer sorted in ascending order
    @param target: integer to find in nums
    @return: index of target in nums if found, -1 if not found
    """
    start = 0
    end = len(nums) - 1

    while start < end:
        mid = (start + end) // 2
        if target <= nums[mid]:
            end = mid
        else:
            start = mid + 1
    
    # start == end ?
    if start == end and target == nums[end]:
        return end
    return -1

def binary_search_template_3(nums, target):
    """
    - Another advanced Binary Search implementation.
    - Search condition needs to access element's left and right neighbors
    - Gurantees Search Space is at least 3 in size at each step
    - Post-processing required. Loop/Recursion ends when there are 2 elements left.

    @param nums: list of integer sorted in ascending order
    @param target: integer to find in nums
    @return: index of target in nums if found, -1 if not found
    """
    if len(nums) == 0:
        return -1
    if len(nums) == 1:
        if target == nums[0]:
            return 0
        return -1
    
    # len(nums) >= 2
    start = 0
    end = len(nums) - 1

    while start + 1 < end:
        mid = (start + end) // 2
        if target <= nums[mid]:
            end = mid
        else:
            start = mid
    
    if target == nums[start]:
        return start
    if target == nums[end]:
        return end
    return -1

def binary_search_insert_position(nums: List[int], target) -> int:
    # find the index where target should be inserted to
    # that is the same as the index after target is inserted to input list
    # e.g. [1, 3, 4], target=2, insertion index is 1
    n = len(nums)
    if n == 0:
        return 0
    if target <= nums[0]:
        return 0
    if target > nums[-1]:
        return n
        
    # n >= 2
    start = 0
    end = n - 1
    while start + 1 < end:
        mid = (start + end) // 2
        if target <= nums[mid]:
            end = mid
        else:
            start = mid

    return end

class TestBinarySearch(unittest.TestCase):
    
    def test_template1(self):
        nums = [0, 3, 6, 7, 9]
        nums2 = [5]
        target1 = 5
        target2 = 6
        self.assertEqual(-1, binary_search_template_1(nums, target1))
        self.assertEqual(2, binary_search_template_1(nums, target2))
        self.assertEqual(0, binary_search_template_1(nums2, target1))
        self.assertEqual(-1, binary_search_template_1([], target2))
    
    def test_template2(self):
        nums = [0, 3, 6, 7, 9]
        nums2 = [5]
        target1 = 5
        target2 = 9
        self.assertEqual(-1, binary_search_template_2(nums, target1))
        self.assertEqual(4, binary_search_template_2(nums, target2))
        self.assertEqual(0, binary_search_template_2(nums2, target1))
        self.assertEqual(-1, binary_search_template_2([], target2))
    
    def test_template3(self):
        nums = [0, 3, 6, 7, 9]
        nums2 = [5]
        target1 = 5
        target2 = 9
        target3 = 6
        target4 = 0
        self.assertEqual(-1, binary_search_template_3(nums, target1))
        self.assertEqual(4, binary_search_template_3(nums, target2))
        self.assertEqual(2, binary_search_template_3(nums, target3))
        self.assertEqual(0, binary_search_template_3(nums, target4))
        self.assertEqual(0, binary_search_template_3(nums2, target1))
        self.assertEqual(-1, binary_search_template_3([], target4))
    
    def test_insert_position(self):
        nums = [0, 3, 6, 7, 9]
        nums2 = [5]
        nums3 = [1, 6]
        target1 = 0
        target2 = 5
        target3 = 10
        self.assertEqual(0, binary_search_insert_position(nums, target1))
        self.assertEqual(2, binary_search_insert_position(nums, target2))
        self.assertEqual(5, binary_search_insert_position(nums, target3))
        self.assertEqual(0, binary_search_insert_position(nums2, target1))
        self.assertEqual(0, binary_search_insert_position(nums2, target2))
        self.assertEqual(1, binary_search_insert_position(nums2, target3))
        self.assertEqual(0, binary_search_insert_position(nums3, target1))
        self.assertEqual(1, binary_search_insert_position(nums3, target2))
        self.assertEqual(2, binary_search_insert_position(nums3, target3))

if __name__ == '__main__':
    unittest.main()
