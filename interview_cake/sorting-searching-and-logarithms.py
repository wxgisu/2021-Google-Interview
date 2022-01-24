from typing import List

# practice
""" 1. Find Rotation Point
Problem
I want to learn some big words so people think I'm smart.

I opened up a dictionary to a page in the middle and started flipping through,
looking for words I didn't know. I put each word I didn't know at increasing
indices in a huge list I created in memory. When I reached the end of the
dictionary, I started from the beginning and did the same thing until I reached
the page I started at.

Now I have a list of words that are mostly alphabetical, except they start
somewhere in the middle of the alphabet, reach the end, and then start from the
beginning of the alphabet. In other words, this is an alphabetically ordered
list that has been "rotated." For example:

  words = ['ptolemaic', 'retrograde', 'supplant', 'undulate', 'xenoepist',
    'asymptote',  # <-- rotates here! 'babka', 'banoffee', 'engender',
    'karpatka', 'othellolagkage',
]

Write a function for finding the index of the "rotation point," which
is where I started working from the beginning of the dictionary. This list is
huge (there are lots of words I don't know) so we want to be efficient here.

Analysis
d, e, f, g, h, a, b, c

g, > d, -> a, b, c
b , < d, a < d -> a
a, <d, g > d -> return a

"""

def find_rotation_point(words: List[str]) -> int:
    num_of_words = len(words)
    reference_word = words[0]
    start_index = 0
    end_index = num_of_words - 1

    while start_index < end_index:
        mid_index = (start_index + end_index) // 2
        mid_word = words[mid_index]
        if mid_word >= reference_word: 
            start_index = mid_index
        else:
            end_index = mid_index
        # print(start_index, end_index)
        if start_index + 1 == end_index:
            if words[start_index] > words[end_index]:
                return end_index
            else:
                break
    return 0

def areInAscendingOrder(word1: str, word2: str) -> bool:
    return word1 < word2

""" 2. Find Repeat, Space Edition
Problem
Find a duplicate, Space Edition™.

We have a list of integers, where:

The integers are in the range 1...n The list has a length of n+1 It
follows that our list has at least one integer which appears at least twice. But
it may have several duplicates, and each duplicate may appear more than twice.

Write a function which finds an integer that appears more than once in our list.
Don't modify the input! (If there are multiple duplicates, you only need to find
one of them.)

We're going to run this function on our new, super-hip MacBook Pro With Retina
Display™. Thing is, the damn thing came with the RAM soldered right to the
motherboard, so we can't upgrade our RAM. So we need to optimize for space!

Analysis
1. two sets duplicated_integers and first_time_seen_integers. 
    for any integer:
        if in duplicated_integers, pass
        else
            if in first_time_seen_integers, remove and add to duplicated_integers
            else add to first_time_seen_integers
    Space O(n) Time O(n)
2. brute force for each integer, check all other integers to see if there are replicates.
    Space O(1) Time O(n^2)
3. 2 is too slow, we can instead sort the input list inplace in O(nlogn) time, then loop
    through sorted list to see if there are two adjacent numbers that are the same. 
    Space (1) Time O(nlogn), but input list is mutated. Can we do this without mutating input?
4. instead of sorting the input array, we can split the integer range into 2 buckets: 1 - 2/n and 2/n+1 - n. 
    Then count number of elements belongs to each bucket, takes the bucket that has more elements that its total
    capacity, and repeat the process
"""

def find_duplicate(numbers: List[int]) -> int:
    length = len(numbers)
    start = 1
    end = length - 1

    while start <= end:
        if start == end:
            return start
        mid = (start + end) // 2
        left_capacity = mid - start + 1
        right_capacity = end - mid
        left_count = right_count = 0
        for number in numbers:
            if start <= number <= mid:
                left_count += 1
            elif mid < number <= end:
                right_count += 1
            else:
                pass
        if left_count > left_capacity:
            end = mid
        elif right_count > right_capacity:
            start = mid + 1
        else:
            raise ValueError(f"Input array length is less than available integers 1 to {length - 1}")
    
    raise NotImplementedError
        
""" 3. Top Scores
Problem
You created a game that is more popular than Angry Birds.

Each round, players receive a score between 0 and 100, which you use to rank
them from highest to lowest. So far you're using an algorithm that sorts in
O(n\lg{n})O(nlgn) time, but players are complaining that their rankings aren't
updated fast enough. You need a faster sorting algorithm.

Write a function that takes:

a list of unsorted_scores the highest_possible_score in the game and returns a
sorted list of scores in less than O(n\lg{n})O(nlgn) time.

For example: unsorted_scores = [37, 89, 41, 65, 91, 53] HIGHEST_POSSIBLE_SCORE =
  100

  # Returns [91, 89, 65, 53, 41, 37]
sort_scores(unsorted_scores, HIGHEST_POSSIBLE_SCORE)

We’re defining n as the number of unsorted_scores because we’re expecting the
number of players to keep climbing.

And, we'll treat highest_possible_score as a constant instead of factoring it
into our big O time and space costs because the highest possible score isn’t
going to change. Even if we do redesign the game a little, the scores will stay
around the same order of magnitude.

Analysis
1. consider using highest score as upper bound to create an array of size highest score.
    Each element is a list of scores same as that index.
    Iterate through the original list to populate the new array.
    Iterate through the new array to get scores in sorted descending order 
2. This method takes O(n) time and O(n) space
3. To optimize, instead of storing a list of scores for each element in new array, 
    we can simply store the count of scores. So 5 at index 4 means there are 5 socres at 4
    in unsorted list. This will reduce new array's size to be O(score). But since we still
    need to store all scores in a new list, the total space is still O(n). If the input list
    if mutatable, then we can rewrite the unsorted input to sorted list, thus reduce total runtime
    to O(score) = O(1) since score is constant.
"""

def get_sorted_scores(unsorted_scores: List[int], max_score: int) -> List[int]:
    num_of_possible_scores = max_score + 1
    scores_dict = [[] for i in range(num_of_possible_scores)]
    sorted_scores = []
    
    for score in unsorted_scores:
        scores_dict[score].append(score)
    
    for i in range(num_of_possible_scores - 1, -1, -1):
        scores = scores_dict[i]
        for score in scores:
            sorted_scores.append(score)
    
    return sorted_scores

def get_sorted_scores_optimized(unsorted_scores: List[int], max_score: int) -> List[int]:
    number_of_possible_scores = max_score + 1
    score_counts = [0] * number_of_possible_scores
    sorted_scores = []
    
    for score in unsorted_scores:
        score_counts[score] += 1
    
    for score in range(number_of_possible_scores - 1, -1, -1):
        count = score_counts[score]
        for i in range(count):
            sorted_scores.append(score)
    
    return sorted_scores
    
"""
[2, 1, 3, 1], 3

scores_dict: 
[
    [], # 0
    [1, 1], # 1
    [2], # 2
    [3], # 3
]

sorted_list: [1, 1, 2, 3]
"""
            
def main():
    # find_rotation_point_test_1 = ['a']
    # find_rotation_point_test_2 = ['a', 'b']
    # find_rotation_point_test_3 = ['c', 'd', 'e', 'f', 'g', 'a', 'b']
    # find_rotation_point_test_4 = ['g', 'a', 'b', 'c', 'd', 'e', 'f']
    # print(find_rotation_point(find_rotation_point_test_1))
    # print(find_rotation_point(find_rotation_point_test_2))
    # print(find_rotation_point(find_rotation_point_test_3))
    # print(find_rotation_point(find_rotation_point_test_4))
    # find_duplicate_test_1 = [1, 2, 5, 4, 6, 3, 4]
    # print(find_duplicate(find_duplicate_test_1))
    get_sorted_scores_test_1 = ([2, 1, 3, 1], 3)
    print(get_sorted_scores(*get_sorted_scores_test_1))
    print(get_sorted_scores_optimized(*get_sorted_scores_test_1))

    

if __name__ == '__main__':
    main()
