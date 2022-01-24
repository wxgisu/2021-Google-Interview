from typing import List, NoReturn, Tuple


# concepts
'''
lists in Python are dynamic arrays
their size double when max length is reached, therefore user don't have to specify length ahead of time
below is comparison between array and dynamic array on runtime/pros/cons

dynamic array:
    runtime:
        - lookup: O(1)
        - append: 
            - average/amortized: O(1) (when doubling size is not needed)
            - worst: O(n) (when doubling size is needed)
        - insert: O(n)
        - delete: O(n)
    pros:
        - variable size
        - fast lookup
        - cache friendly
    cons:
        - slow worst append time: O(n)
        - slow inserts and deletes: O(n)

arrays:
    runtime:
        - lookup: O(1)
        - append: O(1)
        - insert: O(n)
        - delete: O(n)
    pros:
        - fast lookup
        - fast append
        - cache friendly
    cons:
        - fixed size
        - slow inserts and deletes
'''

# implementation
'''
    no need to implement in python. just need to know:
    1. python list is a dynamic array
    2. there's no fix-size array implementation in python
'''

# practices

""" 1. Merging Meeting Times
Problem
Your company built an in-house calendar tool called HiCal. You want to add a
feature to see the times in a day when everyone is available.

To do this, you’ll need to know when any team is having a meeting. In HiCal, a
meeting is stored as a tuple ↴ of integers (start_time, end_time). These
integers represent the number of 30-minute blocks past 9:00am.

For example: (2, 3)  # Meeting from 10:00 – 10:30 am (6, 9)  # Meeting from
12:00 – 1:30 pm

Write a function merge_ranges() that takes a list of multiple meeting time
ranges and returns a list of condensed ranges.

For example, given: [(0, 1), (3, 5), (4, 8), (10, 12), (9, 10)]

your function would return: [(0, 1), (3, 8), (9, 12)]

Analysis
1. to determine if any pair of ranges A and B can merge, only need to see if
   A.start >= B.end
2. if we evaluate all pairs, if can merge, do merge, in worst case, no pairs can
   merge, then takes O(n^2) time to go through all pairs. 
3. but do we need to compare all pairs? say we have 3 ranges A(1, 5), B(6, 10),
   C(3, 7), we can compare AB, AC, (AC)B; or we can compare AC, (AC)B. notice
   the second compare sequence is using only 2 comparisons instead of 3. 
4. this suggest certain sequence of comparison could lead to less num of
   comparisions. looking at the example in 3 closer, we can see that compare AC
   first is better than AB, because A and C have closer start time and therefore
   have a bigger chance of overlapping
5. if we generalize this idea by sorting the input array ascendingly by start
   time, then compare sequencially starting from the ranges with ealist start
   time, this will only require n-1 comparisons and therefore give a O(n)
   algorithm
6. but we first need to prove the algorithm can correctly merge after sorting.
   for the algo to be correct, it must be able to handle following cases: 
   c1: two ranges with same start time (note end time is unsorted)
   c2: two ranges with different start time

   say we have sorted ranges A(1, 5) B(1, 3) C(1, 7) D(2, 4) E(3, 9)
   start at A, B 
   merge A, B -> AB(1,5) C(1, 7) D(2, 4) E(3, 9)
   merge AB, C -> ABC(1, 7) D(2, 4) E(3, 9)
   merge ABC, D -> ABCD(1, 7) E(3, 9)
   merge ABCD, E -> ABCDE(1, 9)
   
   say we have sorted ranges A(1, 5) B(1, 3) C(1, 7) D(2, 4) E(8, 9)
   start  A, B
   merge A, B -> AB(1,5) C(1, 7) D(2, 4) E(8, 9)
   merge AB, C -> ABC(1, 7) D(2, 4) E(8, 9)
   merge ABC, D -> ABCD(1, 7) E(8, 9)
   no need to merge -> ABCD(1, 7) E(8, 9)
   
Data Structure
- list of tuples

Algorithm
- sort

Runtime
- O(n * logn)

Space
- O(n)
"""

def merge_ranges(meetings: List[Tuple[int, int]]) -> List[Tuple[int, int]]:
    sorted_meetings = sorted(meetings)
    merged_meetings = [sorted_meetings[0]]

    for current_meeting_start, current_meeting_end in sorted_meetings[1:]:
        last_merged_meeting_start, last_merged_meeting_end = merged_meetings[-1]
        if last_merged_meeting_end >= current_meeting_start:
            merged_meetings[-1] = (
                last_merged_meeting_start,
                max(current_meeting_end, last_merged_meeting_end),
            )
        else:
            merged_meetings.append(
                (current_meeting_start, current_meeting_end)
            )
    
    return merged_meetings

merge_ranges_test_case_1 = [(1, 5), (1, 3), (1, 7), (2, 4), (3, 9)]
merge_ranges_test_case_2 = [(1, 5), (1, 3), (1, 7), (2, 4), (8, 9)]
merge_ranges_test_case_3 = [(4, 10), (1, 3), (1, 7), (2, 4), (8, 9)]

""" 2. Reverse String in Place
Problem
Write a function that takes a list of characters and reverses the letters in place.

Analysis
1. the first character becomes the last, the last becomes the first
2. the second becomes the second last, the second last becomes the second
3. we can generalize the above 2 points to a pair wise swap between first and
   second half of the list in a mirro reflection manner
4. the center of the mirror would be either 1 char or 2 chars based on odd/even
   number of chars in list

Data Structure
list

Algorithm
1. create two pointers left and right, left start at beginning of list, right
   start at end of list
2. swap chars at left and right pointers
3. move left pointer by 1 position to the right, move right pointer by 1
   position to the left
4. repeat 2, 3 until left pointer >= right pointer

Runtime
O(n)

Space
O(1)
"""

def reverse_string(string_list: List[str]) -> NoReturn:
    left = 0
    right = len(string_list) - 1
    
    while left < right:
        string_list[left], string_list[right] = string_list[right], string_list[left]
        left += 1
        right -= 1

reverse_string_test_case_1 = ['h', 'e', 'l', 'l', 'o']
reverse_string_test_case_2 = ['t', 'e', 's', 't']

""" 3. Merge Sorted Arrays Problem In order to win the prize for most cookies
   sold, my friend Alice and I are going to merge our Girl Scout Cookies orders
   and enter as one unit.

Each order is represented by an "order id" (an integer).

We have our lists of orders sorted numerically already, in lists. Write a
function to merge our lists of orders into one sorted list.

For example: my_list     = [3, 4, 6, 10, 11, 15] alices_list = [1, 5, 8, 12, 14,
19]
# Prints [1, 3, 4, 5, 6, 8, 10, 11, 12, 14, 15, 19]
print(merge_lists(my_list, alices_list))

Analysis
1. This is the same as the merge routein in merge sort
2. A naive solution is to combine two arrays, then re-sort the combined array.
   But this takes O(nlogn) time.
3. The naive solution ignored the fact that the original arrays are already
   sorted. To take advantage of this fact, instead of directly append the whole
   second array after the first array, we can look at the first element in each
   array and take the smaller one. After the smaller one is taken from one
   array, shorten that array by removing the first element (or consider the
   second element as the new first), then we are facing exactly the same problem
   of finding the smaller element between first elements of the two arrays.
   Recursively solve the same problem will solve the whole problem.

Data Structure
- Dynamic Array or Array

Algorithm:
1. Have two pointers, each point at the beginning of the two sorted arrays
2. Take the smaller element pointed by the two pointers, append to combined
   array
3. Increment the smaller element pointer by one
4. Repeat 1,2 until both arrays are exausted

Runtime
- O(n) where n is the total number of elements in the two arrays

Space
- O(n), because a new array is used to store the combined sorted elements
"""

def merge_sorted_arrays(arr1: List[int], arr2: List[int]) -> List[int]:
    merged_arr_len = len(arr1) + len(arr2)
    merged_arr = [None] * merged_arr_len
    
    current_merged_arr_index = 0
    current_arr1_head_index = 0
    current_arr2_head_index = 0
    
    while current_merged_arr_index < merged_arr_len:
        current_arr1_head = get_arr_head(arr1, current_arr1_head_index)
        current_arr2_head = get_arr_head(arr2, current_arr2_head_index)
        if current_arr1_head <= current_arr2_head:
            merged_arr[current_merged_arr_index] = current_arr1_head
            current_arr1_head_index += 1
        else:
            merged_arr[current_merged_arr_index] = current_arr2_head
            current_arr2_head_index += 1
        current_merged_arr_index += 1
            
    print(f"Merged array is: {merged_arr}")
    return merged_arr

def get_arr_head(arr: List[int], index: int) -> int:
    return arr[index] if index < len(arr) else float('inf')

merge_sorted_arrays_test_1 = (
    [1, 3, 5],
    [2, 4, 6],
)
merge_sorted_arrays_test_2 = (
    
)

""" 4. Cafe Order Checker
Problem 
   My cake shop is so popular, I'm adding some tables and hiring wait staff so
   folks can have a cute sit-down cake-eating experience.
   
   I have two registers: one for take-out orders, and the other for the other
   folks eating inside the cafe. All the customer orders get combined into one
   list for the kitchen, where they should be handled first-come, first-served.
   
   Recently, some customers have been complaining that people who placed orders
   after them are getting their food first. Yikes—that's not good for business!
   
   To investigate their claims, one afternoon I sat behind the registers with my
   laptop and recorded:
   - The take-out orders as they were entered into the system and given to the
     kitchen. (take_out_orders)
   - The dine-in orders as they were entered into the system and given to the
     kitchen. (dine_in_orders)
   - Each customer order (from either register) as it was finished by the
     kitchen. (served_orders)
   
   Given all three lists, write a function to check that my service is
   first-come, first-served. All food should come out in the same order
   customers requested it.

Analysis
1. The problem is to check if the two arrays are subsequences of a third array
2. We can simply check if each small array is subsequence of the third array,
   and return Ture only if both are
3. Or we can check if both arrays are subsequences of the third array in one go
   by scanning through the thrid array once. 
4. Assumes order number is globally unique

Data Structure
- only need some variables to store pointers/indexes for the three arrays

Algorithm
1. Have two pointers pointing at head of two short arrays, have another
   pointer pointing at the head of the third array
2. Loop through the third array, for each element, check if the element matches
   either head of the two small arrays, if yes, increment the head pointer of matched small
   array, if no (ie doesn't match neither head elements of the two small
   arrays), validation if failed, return false
3. If the loop successfully finishes, means at any given point, the third
   array's current element always matches the current head of either small
   array, which means both small arrays are subsequences of the third array, return true

Runtime
- O(n) n is length of third array

Space
- O(1)
"""

def check_order(
    take_out_orders: List[int],
    dine_in_orders: List[int],
    served_orders: List[int]
) -> bool:
    current_take_out_order_index = 0
    current_dine_in_order_index = 0
    
    for served_order in served_orders:
        current_take_out_order = (
            take_out_orders[current_take_out_order_index]
            if current_take_out_order_index < len(take_out_orders)
            else None
        )
        current_dine_in_order = (
            dine_in_orders[current_dine_in_order_index]
            if current_dine_in_order_index < len(dine_in_orders)
            else None
        )
        if served_order == current_take_out_order:
            current_take_out_order_index += 1
        elif served_order == current_dine_in_order:
            current_dine_in_order_index += 1
        else:
            return False
        
    return True

check_order_test_1 = (
    [1, 3, 5],
    [2, 4, 6],
    [1, 2, 4, 6, 5, 3],
)
check_order_test_2 = (
    [17, 8, 24],
    [12, 19, 2],
    [17, 8, 12, 19, 24, 2],
)


if __name__ == "__main__":
    # merge_ranges_result_1 = merge_ranges(merge_ranges_test_case_1)
    # merge_ranges_result_2 = merge_ranges(merge_ranges_test_case_2)
    # merge_ranges_result_3 = merge_ranges(merge_ranges_test_case_3)
    # print(merge_ranges_result_1)
    # print(merge_ranges_result_2)
    # print(merge_ranges_result_3)
    
    # reverse_string(reverse_string_test_case_1)
    # reverse_string(reverse_string_test_case_2)
    # print(reverse_string_test_case_1)
    # print(reverse_string_test_case_2)
    
    # merge_sorted_arrays(
    #     merge_sorted_arrays_test_1[0], merge_sorted_arrays_test_1[1]
    # )
    
    # check_order_result_1 = check_order(
    #     check_order_test_1[0],
    #     check_order_test_1[1],
    #     check_order_test_1[2]
    # )
    # check_order_result_2 = check_order(
    #     check_order_test_2[0],
    #     check_order_test_2[1],
    #     check_order_test_2[2]
    # )
    # print(check_order_result_1)
    # print(check_order_result_2)
