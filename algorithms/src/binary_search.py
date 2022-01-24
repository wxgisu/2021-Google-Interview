from typing import List, Tuple

"""
There seems to have multiple patterns/variations for the binary search algorithm. 
1. start = 0, end = length - 1, start = mid + 1 to go right, end = mid - 1 to go left # see if mid is target
2. start = 0, end = length - 1, start = mid to go right, end = mid to go left # see target is between which two adjacent elements
3. start = 0, end = length, start = mid + 1 to go right, end = mid - 1 to go left # search for a cutting pattern from length+1 choices
4. there should be more combinations, but I still can't fully understand what are the differences and when should they be used
more practice is needed
"""
def binary_search(nums: List[int], target) -> bool:
    # throw away mid once confirm it is not target
    length = len(nums)
    start = 0
    end = length -1
    while start <= end:
        mid = (start + end) // 2
        if nums[mid] == target:
            return True
        elif nums[mid] < target:
            start = mid + 1
        else:
            end = mid - 1
        print(start, end)
    return False

def binary_search_2(nums: List[int], target) -> bool:
    # always include mid in the next round of search
    length = len(nums)
    start = 0
    end = length -1
    while start <= end:
        mid = (start + end) // 2
        if nums[mid] == target:
            return True
        elif nums[mid] < target:
            start = mid
        else:
            end = mid
        print(start, end)
        if start + 1 == end:
            if nums[start] == target or nums[end] == target:
                return True
            else:
                break
    return False

def binary_search_insert_position(nums: List[int], target) -> int:
    # find the index where target should be inserted to
    # that is the same as the index after target is inserted to input list
    # e.g. [1, 3, 4], target=2, insertion index is 1
    n = len(nums)
    if target < nums[0]:
        return 0
    if target > nums[-1]:
        return n
    start = 0
    end = n - 1

    while start <= end:
        mid = (start + end) // 2
        if target <= mid:
            end = mid
        else:
            start = mid
        
        if start + 1 == end:
            return end

"""
See behaviors for the three tempaltes here:
/Users/Xiaoguang/Study/knowledge-base/attachments/binary-search-templates.jpg

template_1 ends with invalid (start, end, mid) set, where start > end
tempalte_2 ends with start == end == mid, the end nodes covers all possible index
template_3 ends with start + 1 == end, start == mid, the end nodes start, end covers all possible adjacent index pair, i.e (0,1) (1,2) ... (n-2, n-1)

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
    """

    """
    :type nums: List[int]
    :type target: int
    :rtype: int
    """
    if len(nums) == 0:
        return -1

    left, right = 0, len(nums) - 1
    while left <= right:
        mid = (left + right) // 2
        print(f'left: {left}, right: {right}, mid: {mid}, mid-right-neighbor: {mid + 1}')
        if nums[mid] == target:
            return mid
        elif nums[mid] < target:
            left = mid + 1
        else:
            right = mid - 1
    print(left, right, None)
    print('--------')

    # End Condition: left > right
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
    """

    """
    :type nums: List[int]
    :type target: int
    :rtype: int
    """
    if len(nums) == 0:
        return -1

    left, right = 0, len(nums) - 1 
    while left < right:
        mid = (left + right) // 2
        print(f'left: {left}, right: {right}, mid: {mid}, mid-right-neighbor: {mid + 1}')
        print(nums[mid + 1])
        if nums[mid] == target:
            return mid
        elif nums[mid] < target:
            left = mid + 1
        else:
            right = mid - 1
    print(left, right, None)
    print('--------')
    
    # Post-processing:
    # End Condition: left == right
    if left != len(nums) and nums[left] == target:
        return left
    return -1

def main():
    # print(binary_search([1, 2, 3], 3))
    # print()
    # print(binary_search_2([1, 2, 3], 1))
    
    # binary_search_insert_position_test_1 = ([1, 3, 4, 9], 7)
    # binary_search_insert_position_res_1 = binary_search_insert_position(*binary_search_insert_position_test_1)
    # print(binary_search_insert_position_res_1)

    binary_search_template_2_test_1 = ([1, 3, 4, 5, 6], 0)
    binary_search_template_2_test_2 = ([1, 3, 4, 5, 6], 7)
    binary_search_template_2(*binary_search_template_2_test_1)
    binary_search_template_2(*binary_search_template_2_test_2)

    print()

    # binary_search_template_1_test_1 = ([1, 3, 4, 5, 6], 0)
    # binary_search_template_1_test_2 = ([1, 3, 4, 5, 6], 7)
    # binary_search_template_1(*binary_search_template_1_test_1)
    # binary_search_template_1(*binary_search_template_1_test_2)
    
if __name__ == '__main__':
    main()
