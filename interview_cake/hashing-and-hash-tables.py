from typing import Dict, List
from string import ascii_letters 

# concepts
"""
hash function: data (string, file, etc.) -> hash (fixed-size string or number)
example: MD5

hash collision: multiple data have the same hash value

use cases for hashing:
1. dictonaires
2. prevent man-in-the-middle attacks

strengths:
- fast lookup
- flexible keys
weaknesses:
- slow worst-case lookups
- unordered
- single-directional lookups (key -> value)
- not cache-friendly

hash table: key -> value
hash set: a set of non-duplicate keys

"""

# practices
""" 1. Inflight Entertainment

Problem
You've built an inflight entertainment system with on-demand movie streaming.

Users on longer flights like to start a second movie right when their first one
ends, but they complain that the plane usually lands before they can see the
ending. So you're building a feature for choosing two movies whose total
runtimes will equal the exact flight length.

Write a function that takes an integer flight_length (in minutes) and a list of
integers movie_lengths (in minutes) and returns a boolean indicating whether
there are two numbers in movie_lengths whose sum equals flight_length.

When building your function:

Assume your users will watch exactly two movies Don't make your users watch the
same movie twice Optimize for runtime over memory

Analysis
1. for each movie_length, check if complement_movie_length (flight_length -
   movie_length) is in the movei_lengths list. but this takes O(n^2) time
2. build an array of zeros, fill array with movie_lengths as indexes and 1 as
   value to indicate of that the corresponding movie_length exist. this way, the
   complement_movie_length lookup only takes O(1) time, making total runtime of
   O(n)

Data Structure
- Array

Algorithm
1. find max integer in movie_lengths, call it max_movie_length
2. build array of zeros with length max_movie_length, call it movies_exist
3. for each movie_length as array index, update corresponding array element to 1
4. for each movie_length, check if complement exist using movies_exist array,
   return true when exist

Algorithm Optimized
1. initiate a set, call it movie_lengths_discovered
2. for each movie_length:
    - if complement_movie_length is in movie_lengths_discovered set, return Ture
    - if not, add movie_length to set
"""

def have_two_movies(flight_length: int, movie_lengths: List[int]) -> bool:
    max_movie_length = max(movie_lengths)
    movies_exist = [False] * (max_movie_length + 1)
    for movie_length in movie_lengths:
        movies_exist[movie_length] = True
    for movie_length in movie_lengths:
        complement_movie_length = flight_length - movie_length
        if (complement_movie_length > 0 and
            complement_movie_length != movie_length and
            movies_exist[complement_movie_length]):
            return True
    return False

def have_two_movies_optimized(flight_length: int, movie_lengths: List[int]) -> bool:
    movie_lengths_discovered = set()
    
    for movie_length in movie_lengths:
        complement_movie_length = flight_length - movie_length
        if complement_movie_length in movie_lengths_discovered:
            return True
        movie_lengths_discovered.add(movie_length)
    
    return False

""" 2. Permutation Palindrome

Problem 
Write an efficient function that checks whether any permutation of an
input string is a palindrome. 

You can assume the input string only contains lowercase letters.

Examples:

"civic" should return True 
"ivicc" should return True 
"civil" should return False
"livci" should return False

Analysis
1. For each permutation (O(n!)) permutations), check if is a palindrome (O(n))
2. But if we observe a palindrome, it is actually a mirror reflection of a
   center. The center could either be an empty char (total num of chars is
   even), or a single char (total num of chars is odd). 
3. Based on above observation, intead of asking if every permutation of a string
   is palindrom, we ask if a set of chars can build a palindrome. All we need to
   do is to see if there are floor(n/2) pairs of chars in the set, i.e. at most
   1 unpaired char. If yes, then return True, otherwise False

Data Structure
- set

Algorithm
1. create empty set
2. for each char in string:
    - if exist in set, remove from set
    - if doesn't exist in set, add to set
3. if set size is 0 or 1, return True; otherwise return False
"""

def is_any_permutation_palindrome(string: str) -> bool:
    unpaired_chars = set()
    for char in string:
        if char in unpaired_chars:
            unpaired_chars.remove(char)
        else:
            unpaired_chars.add(char)
    
    if len(unpaired_chars) in (0, 1):
        return True
    return False

""" 3. Word Cloud Data

Problem 
You want to build a word cloud, an infographic where the size of a word
corresponds to how often it appears in the body of text.

To do this, you'll need data. Write code that takes a long string and builds its
word cloud data in a dictionary, where the keys are words and the values are
the number of times the words occurred.

Think about capitalized words. For example, look at these sentences:
'After beating the eggs, Dana read the next step:'
'Add milk and eggs, then add flour and sugar.'

What do we want to do with "After", "Dana", and "add"? In this example, your
final dictionary should include one "Add" or "add" with a value of 2. Make
reasonable (not necessarily perfect) decisions about cases like "After" and
"Dana".

Assume the input will only contain words and standard punctuation.

Analysis
1. Scan through the sentences and add each word (lower case) into dictionary,
   and update count
2. Runtime is O(n) where n is number of chars
3. Space is O(m) where m is number of words, with upper bound of n
4. Can we do any better?

Algorithm
1. create empty set, add a-z A-Z
2. create empty list and empty dict
3. for each char in string:
- if in set
    - convert to lower case
    - append to list
- if not in set
    - concatenate chars in list into word string
    - update/add word count in dict
    - reset list to empty
"""

def count_words(string: str) -> Dict[str, int]:
    letters = set([c for c in ascii_letters])
    word_list = []
    word_counts = {}
    for char in string:
        if char in letters:
            word_list.append(char.lower())
        elif not word_list:
            continue
        else:
            word = ''.join(word_list)
            word_counts[word] = word_counts.get(word, 0) + 1
            word_list.clear()
    if word_list:
        word = ''.join(word_list)
        word_counts[word] = word_counts.get(word, 0) + 1
        
    return word_counts

def main():
    # 1. Inflight Entertainmaint
    # ie_res_1 = have_two_movies(10, [1, 4, 2, 9, 23])
    # ie_res_2 = have_two_movies(3, [2, 3, 7])
    # ie_res_3 = have_two_movies(5, [5, 2, 4])
    # print(ie_res_1, ie_res_2, ie_res_3)

    # ie_res_1 = have_two_movies_optimized(10, [1, 4, 2, 9, 23])
    # ie_res_2 = have_two_movies_optimized(3, [2, 3, 7])
    # ie_res_3 = have_two_movies_optimized(5, [5, 2, 4])
    # print(ie_res_1, ie_res_2, ie_res_3)

    # 2. Permutation Palindrome
    # pp_res_1 = is_any_permutation_palindrome('aak')
    # pp_res_2 = is_any_permutation_palindrome('hello')
    # print(pp_res_1, pp_res_2)

    """
    'aak'
    unpaired_chars: k
    char:
    -> True

    'hello'
    unpaired_chars: h, e, o
    char: o
    -> False
    """
    
    # 3. Word Cloud Data
    wcd_res_1 = count_words('Hi, Jo')
    wcd_res_2 = count_words(': Hi, Jo')
    wcd_res_3 = count_words('This is a test for a very very very long string!!!')
    
    print(wcd_res_1, wcd_res_2, wcd_res_3)

    """
    'hi, Jo'
    word_list: j, o
    word_count: hi: 1, jo: 1
    char: o
    word: jo

    """

if __name__ == '__main__':
    main()
