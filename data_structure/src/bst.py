import sys
sys.path.append("/Users/Xiaoguang/Study/CS/Interviews/2021-Google")
from dataclasses import dataclass
from typing import Optional
from algorithms.src.tree_dfs import dfs_in_iter
import unittest
import copy

@dataclass
class Node:
    name: str
    value: int
    left: Optional['Node'] = None
    right: Optional['Node'] = None
    parent: Optional['Node'] = None

class BinarySearchTree:
    def __init__(self, root: Node):
        self.root = root
        self.validate()
    
    def validate(self):
        root = self.root
        stack = [(root, float('-inf'), float('inf'))] # (node, min, max) 
        while stack:
            node, min, max= stack.pop()
            if node.value < min or node.value > max: 
                raise ValueError("The input tree is invalid binary search tree")
            if node.left: 
                stack.append((node.left, min, node.value))
            if node.right:
                stack.append((node.right, node.value, max))
        return True

    def search(self, k: int) -> Optional[Node]:
        root = self.root
        return self._search(root, k)
    
    def _search(self, root: Node, k: int) -> Optional[Node]:
        if root == None:
            return root
        if k == root.value:
            return root
        elif k < root.value:
            return self._search(root.left, k)
        else:
            return self._search(root.right, k)
    
    def search_iter(self, k: int) -> Optional[Node]:
        node = self.root
        while node != None and node.value != k:
            if k < node.value:
                node = node.left
            else:
                node = node.right
        return node
    
    def find_min(self) -> Optional[Node]:
        node = self.root
        while node and node.left:
            node = node.left
        return node
    
    def find_max(self) -> Optional[Node]:
        node = self.root
        while node and node.right:
            node = node.right
        return node
    
    def find_successor(self, x: Node) -> Optional[Node]:
        if not x:
            return None
        if x.right:
            bst = BinarySearchTree(x.right)
            return bst.find_min()
        y = x.parent
        while y and y.right == x:
            x, y = y, y.parent
        return y

    def find_predecessor(self, x: Node) -> Optional[Node]:
        if not x:
            return None
        if x.left:
            bst = BinarySearchTree(x.left)
            return bst.find_max()
        y = x.parent
        while y and y.left == x:
            x, y = y, y.parent
        return y
    
    def insert(self, k: int):
        node = Node(str(k), k)
        parent = None
        child = self.root
        while child:
            parent = child
            if k < child.value:
                child = child.left
            else:
                child = child.right
        node.parent = parent
        if not parent:
            self.root = node
        if k < parent.value:
            parent.left = node
        else:
            parent.right = node
        return
        
    def delete(self, node: Node):
        if not node.left:
            self._transplant(node, node.right)
        elif not node.right:
            self._transplant(node, node.left)
        else: # both left/right child exist
            successor = self.find_successor(node)
            if node.right != successor:
                self._transplant(successor, successor.right)
                successor.right = node.right
                successor.right.parent = successor
            successor.left = node.left
            successor.left.parent = successor
            self._transplant(node, successor)
        return
    
    def _transplant(self, dest_node: Node, source_node: Node):
        """
        transplant from source to dest, aka replace dest by source
        """
        # change parent -> child pointer
        if not dest_node.parent:
            self.root = source_node
        elif dest_node.parent.left == dest_node:
            dest_node.parent.left = source_node
        else:
            dest_node.parent.right = source_node
        # change child -> parent pointer
        if source_node:
            source_node.parent = dest_node.parent
        return 
    
# trees
''' tree1
         6
       /   \
      5     7
    /   \     \
   2     5     8
'''    
tree1 = Node('6', 6)
tree1.left = Node('5', 5, parent=tree1)
tree1.right = Node('7', 7, parent=tree1)
tree1.left.left = Node('2', 2, parent=tree1.left)
tree1.left.right = Node('5', 5, parent=tree1.left)
tree1.right.right = Node('8', 8, parent=tree1.right)
print('tree1: ', dfs_in_iter(tree1))

''' tree2
         6
       /   \
      10    7
    /   \     \
   2     5     8
'''    
tree2 = Node('6', 6)
tree2.left = Node('10', 10, parent=tree2)
tree2.right = Node('7', 7, parent=tree2)
tree2.left.left = Node('2', 2, parent=tree2.left)
tree2.left.right = Node('5', 5, parent=tree2.left)
tree2.right.right = Node('8', 8, parent=tree2.right)
print('tree2: ', dfs_in_iter(tree2))

class TestBinarySearchTree(unittest.TestCase):
    def test_validate_1(self):
        tree = copy.deepcopy(tree1)
        bst = BinarySearchTree(tree)
        self.assertTrue(bst.validate())
    
    def test_validate_2(self):
        self.assertRaises(ValueError, BinarySearchTree, tree2)
    
    def test_search(self):
        tree = copy.deepcopy(tree1)
        bst = BinarySearchTree(tree)
        hit_node = tree.left.left
        hit_node2 = tree.left
        self.assertEqual(bst.search(2), hit_node)
        self.assertEqual(bst.search(5), hit_node2)
        self.assertEqual(bst.search(9), None)
    
    def test_search_iter(self):
        tree = copy.deepcopy(tree1)
        bst = BinarySearchTree(tree)
        hit_node = tree.left.left
        hit_node2 = tree.left
        self.assertEqual(bst.search_iter(2), hit_node)
        self.assertEqual(bst.search_iter(5), hit_node2)
        self.assertEqual(bst.search_iter(9), None)
    
    def test_find_min(self):
        tree = copy.deepcopy(tree1)
        bst = BinarySearchTree(tree)
        self.assertEqual(bst.find_min(), tree.left.left)
    
    def test_find_max(self):
        tree = copy.deepcopy(tree1)
        bst = BinarySearchTree(tree)
        self.assertEqual(bst.find_max(), tree.right.right)
    
    def test_find_successor(self):
        tree = copy.deepcopy(tree1)
        bst = BinarySearchTree(tree)
        self.assertEqual(bst.find_successor(tree), tree.right)
        self.assertEqual(bst.find_successor(tree.left.right), tree)
        
    def test_find_predecessor(self):
        tree = copy.deepcopy(tree1)
        bst = BinarySearchTree(tree)
        self.assertEqual(bst.find_predecessor(tree), tree.left.right)
        self.assertEqual(bst.find_predecessor(tree.left.left), None)
        self.assertEqual(bst.find_predecessor(tree.right.right), tree.right)
    
    def test_insert(self):
        bst = BinarySearchTree(copy.deepcopy(tree1))
        bst.insert(4)
        self.assertEqual(bst.root.left.left.right.value, 4)
    
    def test_delete(self):
        bst = BinarySearchTree(copy.deepcopy(tree1))
        bst.delete(bst.root)
        self.assertEqual(bst.root.value, 7)

        bst2 = BinarySearchTree(copy.deepcopy(tree1))
        bst2.delete(bst2.root.left)
        self.assertEqual(bst2.root.left.value, 5)
        self.assertEqual(bst2.root.left.right, None)

if __name__ == '__main__':
    unittest.main()
