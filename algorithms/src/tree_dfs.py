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
    result = []
    dfs_pre_visit(root, result)
    return result

def dfs_pre_visit(root: Node, result: List[str]):
    if root == None:
        return
    result.append(root.name)
    dfs_pre_visit(root.left, result)
    dfs_pre_visit(root.right, result)
    return
    
def dfs_in(root: Node):
    result = []
    dfs_in_visit(root, result)
    return result

def dfs_in_visit(root: Node, result: List[str]):
    if root == None:
        return
    dfs_in_visit(root.left, result)
    result.append(root.name)
    dfs_in_visit(root.right, result)
    return

def dfs_post(root: Node):
    result = []
    dfs_post_visit(root, result)
    return result

def dfs_post_visit(root: Node, result: List[str]):
    if root == None:
        return
    dfs_post_visit(root.left, result)
    dfs_post_visit(root.right, result)
    result.append(root.name)
    
def dfs_pre_iter(root: Node):
    result = []
    if root == None:
        return result

    stack = []
    current = root
    while stack or current: 
        if current:
            result.append(current.name)
            stack.append(current.right)
            current = current.left
        else:
            current = stack.pop()

    return result

def dfs_in_iter(root: Node):
    result = []
    if root == None:
        return result

    stack = []
    current = root
    while stack or current:
        if current:
            stack.append(current)
            current = current.left
        else:
            current = stack.pop()
            result.append(current.name)
            current = current.right

    return result

def dfs_post_iter(root: Node):
    result = []
    if root == None:
        return result
    
    parent = [] 
    right_child = []
    current = root

    while parent or current:
        if current:
            parent.append(current)
            if current.right:
                right_child.append(current.right)
            current = current.left
        else:
            if right_child and right_child[-1] == parent[-1].right:
                current = right_child.pop()
            else:
                current = parent.pop()
                result.append(current.name)
                current = None
    
    return result

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
        
    
    

    
    


