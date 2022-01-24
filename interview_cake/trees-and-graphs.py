from collections import deque, namedtuple
from typing import List, Dict, NamedTuple, Optional

# concepts
"""
A Binary tree is a tree where each node has at most 2 childern.

1                    10

2                5          12

4            3       2   9       7 perfect tree

hight = h num_of_nodes = n

n = 2^0 + 2^1 + 2^2 + ... + 2^(h-1) 2n = 2^1 + 2^2 + ... + 2^(h-1) + 2^h -> n =
2^h - 1 = 2^(h-1) * 2 - 1

So the last level have 1 more node than the sum of all other levels


Graph Nodes connected with edges representing an interconnected network


Undirected Graph

A -- B -- C
     |    |
     |    |
     D ---|

Directed Graph

A -> B -> C -> D
     |         ^
     |---------|

A -> B -> C
     ↓    ↓
     D <- +

"""

# practices
""" 1. Balanced Binary Tree

Write a function to see if a binary tree is "superbalanced" (a new tree
property we just made up).

A tree is "superbalanced" if the difference between the depths of any two leaf
nodes ↴ is no greater than one.


                A

            B       C

          D   E   F   G       

                     H  I
                     
Naive Solution:
- Traverse the tree with dfs, 
    - When at a leaf node, record the depth count
    - Recorde the max / min depth so far
    - When ever (max - min) > 1, return false
"""

from typing import Tuple


class Node(object):

    def __init__(self, value):
        self.value = value
        self.left = None
        self.right = None
        
    def insert_left(self, value):
        self.left = Node(value)
        return self.left
    
    def insert_right(self, value):
        self.right = Node(value)
        return self.right
    

def is_balanced(root: Node) -> bool:
    max, min = dfs(root, 0, float('-inf'), float('inf'))
    return False if max - min > 1 else True

def dfs(root: Node, 
        depth: int, 
        max_depth: int, 
        min_depth: int
        ) -> Tuple[int, int]:
    if root == None:
        return (max_depth, min_depth)
    print(root.value, depth)
    
    if root.left == root.right == None:
        if depth > max_depth:
            max_depth = depth
        if depth < min_depth:
            min_depth = depth
        return (max_depth, min_depth)
    
    left_max, left_min = dfs(root.left, depth + 1, max_depth, min_depth)
    right_max, right_min = dfs(root.right, depth + 1, max_depth, min_depth)
    
    return (max(left_max, right_max),
            min(left_min, right_min))

"""
            A

        B       C
              
              D    E
(A, 0, -inf, inf) // left_man, left_min = 1, 1, right_max, right_min = 2,2
-> (1, 2)
"""

def is_leaf_node(node: Node) -> bool:
    return (not node.left) and (not node.right)

def is_balanced_iterative(root: Node) -> bool:
    if is_leaf_node(root):
        return True
    
    max_depth = float('-inf') 
    min_depth = float('inf')
    stack = []
    
    stack.append((root, 0))
    
    while stack:
        node,depth = stack.pop()
        
        # leaf node
        if is_leaf_node(node):
            max_depth = max(max_depth, depth)
            min_depth = min(min_depth, depth)
            if (max_depth - min_depth) > 1:
                return False
        
        # non left node
        if node.left:
            stack.append((node.left, depth + 1))
        if node.right:
            stack.append((node.right, depth + 1))
            
    return True

"""
                A

            B       C

                        D


max_depth: 2
min_depth: 1
stack: []
node,depth: B, 1

-> True
"""

""" 2. Validate Bainary Serach Tree
Problem
Write a function to check that a binary tree ↴ is a valid binary search tree.

Algo
- As traversing the tree, use the parent's value to updat the max/min value for all nodes in the subtree rooted 
by parent's left/right child
- When ever a node is not within the max/min range, return False. 
- If no node returns False, return True

Alternative Algo
- In order traverse the tree and store all nodes in an array
- For each element in the array at index i, make sure  array[i-1] <= array[i] < array[i+1]

"""
def is_binary_search_tree(root: Node) -> bool:
    stack = []
    stack.append((root, float('inf'), float('-inf')))
    
    while stack:
        node, max, min = stack.pop()
        if (node.value <= min) or (node.value > max):
            return False
        
        if node.left:
            stack.append((node.left, node.value, min))
        
        if node.right:
            stack.append((node.right, max, node.value))

    return True

""" 3. 2nd Largest Item in a Binary Serach Tree

Algo
- Starting from root, walk to the right, until there's no right node, that node is the largest node
- Then there are two possibilities:
    - 1. the largest node has no left node, in that case, the second largest node is its parent
    - 2. the largest node has left node, in that case, the second largest node is the largest node of of the tree rooted at its left node

"""

def get_largest_value_in_bst(root: Node) -> int:
    while root.right:
        root = root.right
    return root.value

def get_second_largest_value_in_bst(root: Node) -> int:
    if (not root) or (not root.left and not root.right):
        raise ValueError

    parent = None
    while root.right:
        parent = root
        root = root.right

    if root.left:
        return get_largest_value_in_bst(root.left)
    
    return parent.value

""" 4. Graph Coloring
Given an undirected graph ↴ with maximum degree ↴ D, find a graph coloring ↴ using at most D+1 colors.

Algo:
- For each node in graph:
    - Find first available leagle color to color the node
"""
class GraphNode:
    def __init__(self, id: int, neighbors: List[int], color: str = None):
        self.id = id
        self.neighbors = neighbors
        self.color = color

def graph_color(graph: List[GraphNode], colors: List[str]) -> List[str]:
    for node in graph:
        neighbor_ids = node.neighbors
        if node in neighbor_ids:
            raise ValueError
        
        leagle_colors = set(colors)
        for neighbor_id in neighbor_ids:
            neighbor = graph[neighbor_id]
            if neighbor.color:
                leagle_colors.remove(neighbor.color)
        node.color = next(iter(leagle_colors))
        print(node.color)
        
""" 5. MeshMessage
https://www.interviewcake.com/question/python3/mesh-message?course=fc1&section=trees-graphs

Single source shortest path in unweighted graph -> BFS
"""
class GraphNode2(NamedTuple):
    id: str
    parent: NamedTuple

def find_shortest_path(graph: Dict[str, List[str]], source: str, target: str) -> Optional[List[str]]:
    queue = deque([])
    queue.append(GraphNode2(source, None))
    visited = set()
    
    while queue:
        current_node = queue.popleft()
        if current_node.id in visited:
            continue
        visited.add(current_node.id)
        for neighbor_id in graph[current_node.id]:
            neighbor_node = GraphNode2(neighbor_id, current_node)
            if neighbor_id == target:
                return get_path(neighbor_node)
            if neighbor_id not in visited:
                queue.append(neighbor_node)
                
    return None

def get_path(node: GraphNode2) -> List[str]:
    path = deque([])
    while node.parent:
        path.appendleft(node.id)
        node = node.parent
    path.appendleft(node.id)
    return list(path)
    


def main():
    n1 = Node(2)
    n1.insert_left(1)
    n1.insert_right(3)
    n1.right.insert_left(4)
    n1.right.insert_right(5)
    n1.right.right.insert_right(6)
    
    n2 = Node(5)
    n2.insert_left(3)
    n2.insert_right(9)
    n2.left.insert_left(2)
    n2.left.insert_right(4)
    n2.right.insert_left(6)
    n2.right.insert_right(11)

    res1 = is_balanced(n1)
    print(res1)

    res2 = is_balanced_iterative(n1)
    print(res2)
    
    res3 = is_binary_search_tree(n1)
    print(res3)
    res4 = is_binary_search_tree(n2)
    print(res4)

    res5 = get_largest_value_in_bst(n2)
    res6 = get_second_largest_value_in_bst(n2)

    print(res5)
    print(res6)
    
    graph = [
        GraphNode(0, [1]),
        GraphNode(1, [0, 2]),
        GraphNode(2, [1])
    ]
    
    colors = ['red', 'blue']
    graph_color(graph, colors)
    
    network = {
        'Min'     : ['William', 'Jayden', 'Omar'],
        'William' : ['Min', 'Noam'],
        'Jayden'  : ['Min', 'Amelia', 'Ren', 'Noam'],
        'Ren'     : ['Jayden', 'Omar'],
        'Amelia'  : ['Jayden', 'Adam', 'Miguel'],
        'Adam'    : ['Amelia', 'Miguel', 'Sofia', 'Lucas'],
        'Miguel'  : ['Amelia', 'Adam', 'Liam', 'Nathan'],
        'Noam'    : ['Nathan', 'Jayden', 'William'],
        'Omar'    : ['Ren', 'Min', 'Scott'],
    }
    res7 = find_shortest_path(network, 'Jayden', 'Jayden')
    print(res7)



    
if __name__ == '__main__':
    main()


    
        
        
        



