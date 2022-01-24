from dataclasses import dataclass
from typing import Optional, List
import unittest

@dataclass
class Node:
    name: str
    value: int = 0
    left: Optional['Node'] = None
    right: Optional['Node'] = None

def dfs_pre(root: Node):
    pass

def dfs_pre_visit(root: Node, result: List[str]):
    pass
    
def dfs_in(root: Node):
    pass

def dfs_in_visit(root: Node, result: List[str]):
    pass

def dfs_post(root: Node):
    pass

def dfs_post_visit(root: Node, result: List[str]):
    pass
    
def dfs_pre_iter(root: Node):
    pass

def dfs_in_iter(root: Node):
    pass

def dfs_post_iter(root: Node):
    pass

# Trees
'''
         A
       /   \
      B     E
    /   \
   C     D
'''
n1 = Node('A')
n2 = Node('B')
n3 = Node('E')
n4 = Node('C')
n5 = Node('D')
tree1 = n1
tree1 = n1
tree1 = n1
tree1.left = n2
tree1.right = n3
tree1.left.left = n4
tree1.left.right = n5

class TestTreeDfs(unittest.TestCase):
    def test_dfs_pre(self):
        actual = dfs_pre(tree1)
        expected = ['A', 'B', 'C', 'D', 'E']
        self.assertEqual(actual, expected)
    
    def test_dfs_in(self):
        actual = dfs_in(tree1)
        expected = ['C', 'B', 'D', 'A', 'E']
        self.assertEqual(actual, expected)
    
    def test_dfs_post(self):
        actual = dfs_post(tree1)
        expected = ['C', 'D', 'B', 'E', 'A']
        self.assertEqual(actual, expected)
        
    def test_dfs_pre_iter(self):
        actual = dfs_pre_iter(tree1)
        expected = ['A', 'B', 'C', 'D', 'E']
        self.assertEqual(actual, expected)
        
    def test_dfs_in_iter(self):
        actual = dfs_in_iter(tree1)
        expected = ['C', 'B', 'D', 'A', 'E']
        self.assertEqual(actual, expected)
        
    def test_dfs_post_iter(self):
        actual = dfs_post_iter(tree1)
        expected = ['C', 'D', 'B', 'E', 'A']
        self.assertEqual(actual, expected)
        
if __name__ == '__main__':
    unittest.main()
        
    
    

    
    


