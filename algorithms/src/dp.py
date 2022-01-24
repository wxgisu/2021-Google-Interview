import unittest
from typing import List


"""
Subproblems for strings/sequences
- suffixes x[i:]
- prefixes x[:i]
- substrings s[i:j]
"""
def fibonacci(n: int) -> int:
    """
    given n, returns the nth fibonacci number
    """
    if n < 1: 
        raise ValueError("n need to be an integer that is at least 1")
    result = [1] * (n + 1)
    if n <= 2:
        return result[n]
    for i in range(3, n + 1):
        result[i] = result[i-1] + result[i-2]
    return result[n]

def single_souce_shortest_path(graph, node):
    # topological_sort
    # sp[v] = min( (sp[u] + weight(u, v)) for all u)
    pass

def text_justification(words: List[str], page_length: int) -> List[str]:
    """
    given list of words, return list of sentences such that each sentence is an optimum line
    what is optimum? minimum badness
    what is badness? (page_length - line_length)^3 if line fits else infinite
    
    @param words: list of words
    @param page_length: max number of charachters in each line
    @return: a list of lines, each line cancatenated by words with space in between
    """ 
    # subproblem: define table[i] as the min badness of subarry words[i:] (call this the suffix)
    # base case: table[n], the min badness of an empty array of words = 0
    # recurrence: table[i] = min(table[j] + badness(i, j) for j = i+1 to n) 
    # note: badness(i, j) is badness of words[i:j] i.e. not including j
    n = len(words)
    table = [(0, None) for i in range(n + 1)]
    for i in range(n-1, -1, -1):
        min_badness = float('inf')
        parent = None
        for j in range(i+1, n+1):
            badness = get_badness(words, i, j, page_length) + table[j][0]
            if badness < min_badness:
                min_badness = badness
                parent = j
        table[i] = (min_badness, parent)
    return table[0]

def get_badness(words, i, j, page_length):
    line_length = sum([len(word) for word in words[i:j]]) + (j - i - 1)
    badness = float('inf') \
        if page_length < line_length \
        else (page_length - line_length) ** 3
    return badness

def parenthesization(sizes: List[int]) -> int:
    """
    @param sizes: list of length n+1 representing sizes of n chained matrixes, e.g. sizes[0] x sizes[1] is 1st matrix size
    @return minimum cost by adding parentheses around matrixes to determine the optimum multiplication sequence
    """
    # subproblem: table[i, j] is the minimum cost for multiplying the ith to jth matrixes
    # guesses: k as the last multiplication point for i <= k <= j-1, i.e. last multiply result of (i to k) and result of (k+1 to j)
    # recurrence: table[i, j] = min( table[i, k] + table[k+1, j] + sizes[i-1] * sizes[k] * sizes[j] for k in range(i, j) )
    # base case: table[i, i] = 0
    n = len(sizes) - 1
    table = [[0] * (n + 1) for i in range(n+1)]
    for window in range(2, n+1):
        for start in range(1, n - window + 2):
            end = start + window - 1
            min_cost = float('inf')
            for k in range(start, end):
                cost = table[start][k] + table[k+1][end] + sizes[start-1] * sizes[k] * sizes[end]
                if cost < min_cost:
                    min_cost = cost
            table[start][end] = min_cost
    return table[1][n]

def edit_distance(x: str, y: str) -> int:
    
    """
    @param x: string to edit
    @paran y: string to become
    @return: integer representing minimum edit distance between x and y

    editing actions and cost:
    - insert: 1
    - delete: 1
    - replace: 0 if two chars are the same else inf
    
    x = "ab", y = "ac"
      j   a   b  
    i 0   1   2
        ↘
    a 1   0 → 1 
          ↓   ↓
    c 2   1 → 2
    """
    distance = [ [0] * (len(x) + 1) for i in range(len(y) + 1)]
    parent = [ [None] * (len(x) + 1) for i in range(len(y) + 1)]
    for i in range(len(x) + 1):
        distance[0][i] = i
        if i > 0:
            parent[0][i] = ((0, i-1), "delete")
    for i in range(len(y) + 1):
        distance[i][0] = i
        if i > 0:
            parent[i][0] = ((i-1, 0), "insert")
    
    for y_id in range(1, len(y) + 1):
        for x_id in range(1, len(x) + 1):
            insert_cost = distance[y_id-1][x_id] + 1
            delete_cost = distance[y_id][x_id-1] + 1
            replace_cost = distance[y_id-1][x_id-1] if y[y_id-1] == x[x_id-1] else float('inf')
            distance[y_id][x_id] = min(insert_cost, delete_cost, replace_cost)
            if distance[y_id][x_id] == insert_cost:
                parent[y_id][x_id] = ((y_id-1, x_id), "insert")
            elif distance[y_id][x_id] == delete_cost:
                parent[y_id][x_id] = ((y_id, x_id-1), "delete")
            else:
                parent[y_id][x_id] = ((y_id-1, x_id-1), "hold")
                
    y_id = len(y)
    x_id = len(x)
    path = []
    while parent[y_id][x_id]:
        parent_location, action = parent[y_id][x_id]
        target_char = y[y_id-1] if action == "insert" else x[x_id-1]
        path.append(f"{action} {target_char}")
        y_id, x_id = parent_location
    path.reverse()
    # print(path)
    return distance[len(y)][len(x)]

def longest_common_subsequence(x: str, y: str) -> int:
    """
    given two strings x and y, return number of characters in the longest common subsequence

    example1: x = "abcd", y = "bed" -> 2 
    example2: x= "", y = "test" -> 0
    """
    # subproblem: table[i][j] length of longest common subsequence for x[0 : i+1] and y[0 : j+1]
    # recurrence: table[i][j] = max(table[i-1][j], table[i][j-1], table[i-1][j-1] + match)
    # base case: table[0][j] = table[i][0] = 0
    # original problem: table[len(y)][len(x)]
    if len(x) == 0 or len(y) == 0:
        return 0
    
    table = [[0] * (len(x) + 1) for i in range(len(y) + 1)]
    parent = [[None] * (len(x) + 1) for i in range(len(y) + 1)]
    for y_id in range(1, len(y) + 1):
        for x_id in range(1, len(x) + 1):
            up = table[y_id - 1][x_id]
            left = table[y_id][x_id - 1]
            up_left = table[y_id - 1][x_id - 1] + 1 \
                if y[y_id - 1] == x[x_id - 1] \
                else float("-inf")
            table[y_id][x_id] = max(up, left, up_left)
            if table[y_id][x_id] == up:
                parent[y_id][x_id] = (y_id - 1, x_id)
            elif table[y_id][x_id] == left:
                parent[y_id][x_id] = (y_id, x_id - 1)
            else:
                parent[y_id][x_id] = (y_id - 1, x_id - 1)
    
    y_id, x_id = len(y), len(x)
    result = []
    while parent[y_id][x_id]:
        if y[y_id - 1] == x[x_id - 1]:
            result.append(y[y_id - 1])
        y_id, x_id = parent[y_id][x_id]
    result.reverse()
    # print(result)
    return table[len(y)][len(x)]

def longest_common_substring(x: str, y: str) -> int:
    """
    given string x and y, return length of longest common substring between x and y

    example1: x = "hello", y = "he" -> 2
    example2: x = "hello", y = "ho" -> 1
    """
    # subproblem: table[i][j] length of longest common substring between y[0 : i+1] and x[0 : j+1] ending at y[i] and x[j]
    # recurrence: table[i][j] = table[i-1][j-1] + 1 if x[i-1] == y[j-1] else 0
    # base case: table[0][i] = table[j][0] = 0
    # original problem: max(table[i][j])

    if len(x) == 0 or len(y) == 0:
        return 0
    
    table = [[0] * (len(x) + 1) for i in range(len(y) + 1)]
    max_length = 0
    max_end_loc = (0, 0)
    for y_id in range(len(y) + 1):
        for x_id in range(len(x) + 1):
            table[y_id][x_id] = table[y_id - 1][x_id - 1] + 1 \
                if y[y_id - 1] == x[x_id -1] \
                else 0
            if table[y_id][x_id] > max_length:
                max_length = table[y_id][x_id]
                max_end_loc = (y_id, x_id)
    rest = max_length
    y_id, x_id = max_end_loc
    result = []
    while rest != 0:
        result.append(y[y_id - 1])
        rest -= 1
        y_id -= 1
    result.reverse()
    # print(result)
    return max_length

def knapsack(sizes: List[int], values: List[int], capacity: int):
    """
    given list of items, each item has attribute of size and value and a knapsack of given size,
    choose items that fit in the knapsack that have max total value
    @param sizes: list of size, one for each item
    @param values: list of value, one for each item
    @param capacity: size of knapsack
    
    sizes: [2, 1, 5]
    values:[3, 2, 4]
    capacity: 5
         
       item 1   2   3 
    cp 0    0   0   0

    1  0    0   0   0
               ↘
    2  0    0   2 → 2      
           ↘
    3  0    3 → 3 → 3 
           ↘       ↘
    4  0    3 → 3   4  
           ↘   ↘
    5  0    3   5 → 5  

    """
    # subproblem: table[i][j] max total value with knapsack of size i and items 1 to j
    # recurrence: 
    #   - table[i][j] = max(table[i][j-1], table[i - sizes[j]][j-1] + values[j]) if sizes[j] <= i
    #   - table[i][j] = table[i][j-1]                                            if sizes[j] > i
    # base case: table[i][0] = table[0][j] = 0
    num_items = len(sizes)
    table = [[0] * (num_items + 1) for i in range(capacity + 1)]
    for cp in range(1, capacity + 1):
        for item in range(1, num_items + 1):
            item_size = sizes[item-1]
            item_value = values[item-1]
            total_value_without_item = table[cp][item-1]
            if item_size <= cp:
                total_value_with_item = table[cp-item_size][item-1] + item_value
                table[cp][item] = max(total_value_without_item, total_value_with_item)
            else:
                table[cp][item] = total_value_without_item
    print(table)
    return table[capacity][num_items]
    
class TestDp(unittest.TestCase):
    
    def test_fibonacci(self):
        self.assertEqual(1, fibonacci(1))
        self.assertEqual(1, fibonacci(2))
        self.assertEqual(2, fibonacci(3))
        self.assertEqual(3, fibonacci(4))
        self.assertEqual(5, fibonacci(5))

    def test_text_justification(self):
        words = ["hello", "world", "and", "earth"]
        page_length = 9
        self.assertEqual(text_justification(words, page_length), (128, 1))

    def test_parenthesization(self):
        sizes = [5, 1, 3, 1]
        self.assertEqual(8, parenthesization(sizes))

    def test_edit_distance(self):
        x = "hello"
        y = "hela"
        self.assertEqual(3, edit_distance(x, y))
    
    def test_longest_common_subsequence(self):
        x = "hi"
        y = "habic"
        self.assertEqual(2, longest_common_subsequence(x, y))
        
    def test_longest_common_substring(self):
        x = "hello"
        y = "he"
        self.assertEqual(2, longest_common_substring(x, y))

    def test_knapsack(self):
        sizes = [2, 1, 5]
        values = [3, 2, 4]
        capacity = 5
        self.assertEqual(5, knapsack(sizes, values, capacity))

if __name__ == "__main__":
    unittest.main()
