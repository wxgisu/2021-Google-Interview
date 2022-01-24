
from dataclasses import dataclass
from typing import ClassVar, Optional
import unittest
import copy

@dataclass
class Node:
    height: int = 0
    bal_factor: int = 0
    value: Optional[int] = None
    left: Optional['Node'] = None
    right: Optional['Node'] = None
    parent: Optional['Node'] = None

class AvlTree:

    NONE = Node(-1, 0)

    def __init__(self, node: Node):
        self.root = node
        self.validate_bst()
        self.populate_hight_and_validate_avl()
    
    @staticmethod
    def dfs_in_order(node: Node, verbose=False):
        result = []
        stack = []
        current = node
        if verbose:
            print("value    height    bal_factor    left    right    parent")
        while stack or current:
            if current:
                stack.append(current)
                current = current.left
            else:
                current = stack.pop()
                result.append(current.value)
                if verbose and current != Node(-1, 0):
                    tab = "    "
                    left = current.left.value if current.left else current.left
                    right = current.right.value if current.right else current.right
                    parent = current.parent.value if current.parent else current.parent
                    print(
                        current.value, tab, \
                        current.height, tab, \
                        current.bal_factor, tab, \
                        left, tab, \
                        right, tab, \
                        parent, tab)
                current = current.right
        return result

    def validate_bst(self):
        # pre-order traversal
        root = self.root
        stack = [(root, float('-inf'), float('inf'))]
        while stack:
            node, min_val, max_val = stack.pop()
            if node.value < min_val or node.value > max_val:
                raise ValueError("Input tree is not a valid binary search tree")
            if node.left:
                stack.append((node.left, min_val, node.value))
            if node.right:
                stack.append((node.right, node.value, max_val))
        return
    
    def populate_hight_and_validate_avl(self):
        # post-order traversal
        parent_stack = []
        right_stack = []
        current = self.root
        while parent_stack or current:
            if current:
                parent_stack.append(current)
                if current.right:
                    right_stack.append(current.right)
                current = current.left
            elif right_stack and parent_stack[-1].right == right_stack[-1]:
                current = right_stack.pop()
            else:
                current = parent_stack.pop()
                if not current.left:
                    current.left = self.NONE
                if not current.right:
                    current.right = self.NONE
                current.height = max(current.left.height, current.right.height) + 1
                current.bal_factor = current.left.height - current.right.height
                if current.bal_factor < -1 or current.bal_factor > 1:
                    raise ValueError("Input tree is not a valid AVL tree")
                current = None
        return

    def search(self, target: int) -> Optional[Node]:
        current = self.root
        while current.value != None:
            if target == current.value:
                return current
            elif target < current.value:
                current = current.left
            else:
                current = current.right
        return None
        
    def find_max(self, node: Node) -> Node:
        if not node:
            raise ValueError("Input node is None")
        current = node
        while current.right.value:
            current = current.right
        return current

    def find_min(self, node: Node) -> Node:
        if not node:
            raise ValueError("Input node is None")
        current = node
        while current.left.value:
            current = current.left
        return current

    def find_successor(self, node: Node) -> Optional[Node]:
        if node.right.value: # right subtree exist
            return self.find_min(node.right)
        
        parent = node.parent
        while parent and parent.right == node:
            node = parent
            parent = parent.parent
        return parent

    def find_predecessor(self, node:Node) -> Optional[Node]:
        if node.left.value: # left subtree exist
            return self.find_max(node.left)
        parent = node.parent
        while parent and parent.left == node:
            node = parent
            parent = parent.parent
        return parent

    def insert(self, node: Node):
        node.height = node.bal_factor = 0
        node.left = node.right = self.NONE

        parent = None
        current = self.root
        while current and current.value:
            parent = current 
            if node.value < current.value:
                current = current.left
            else:
                current = current.right
        node.parent = parent
        if not parent:
            self.root = node
        elif node.value < parent.value:
            parent.left = node
        else:
            parent.right = node
        
        # fix height
        self._fix_height_above_node(node)

        # re-balance
        self._rebalance(node) 
        return

    def delete(self, node:Node):
        if not node.left.value and not node.right.value:
            node_to_fix = node.parent
            self._transplant(node, self.NONE)
        elif not node.left.value:
            node_to_fix = node.right
            self._transplant(node, node.right)
        elif not node.right.value:
            node_to_fix = node.left
            self._transplant(node, node.left)
        else: # both children exist
            successor = self.find_successor(node)
            node_to_fix = successor
            if node.right != successor:
                self._transplant(successor, successor.right)
                successor.right = node.right
                successor.right.parent = successor
                node_to_fix = successor.right
            self._transplant(node, successor)
            successor.left = node.left
            successor.left.parent = successor
        if node_to_fix:
            self._fix_height_above_node(node_to_fix)
            self._rebalance(node_to_fix)
        return
    
    def _fix_height_above_node(self, node: Node):
        current = node
        while current:
            self._update_height_and_bal_factor(current)
            current = current.parent
        return

    def _rebalance(self, node: Node):
        current = node
        while current:
            # height and bal_factor need to be updated because it might have changed in prev iteration
            self._update_height_and_bal_factor(current)
            
            # if balanced, move up
            if -1 <= current.bal_factor <= 1:
                current = current.parent
                continue
            
            # if not balanced
            ## first figure out case
            if current.bal_factor > 0:
                level1 = 'left'
                if current.left.bal_factor > 0:
                    level2 = 'left'
                else:
                    level2 = 'right'
            else:
                level1 = 'right'
                if current.right.bal_factor > 0:
                    level2 = 'left'
                else:
                    level2 = 'right'
            ## then fix based on case
            if (level1, level2) == ('left', 'left'):
                self._right_rotate(current)
            elif (level1, level2) == ('left', 'right'):
                self._left_rotate(current.left)
                self._right_rotate(current)
            elif (level1, level2) == ('right', 'left'):
                self._right_rotate(current.right)
                self._left_rotate(current)
            else:
                self._left_rotate(current)
            current = current.parent.parent
        return

    def _left_rotate(self, node:Node):
        right = node.right
        # node adopt right child's left child as its new right child
        node.right = node.right.left
        if node.right.value:
            node.right.parent = node
        # node's parent becomes right child's parent
        if not node.parent:
            self.root = right
        elif node.parent.left == node:
            node.parent.left = right
        else:
            node.parent.right = right
        right.parent = node.parent
        # node becomes right child's left child
        right.left = node
        node.parent = right
        # fix height and bal_factor
        self._update_height_and_bal_factor(node)
        self._update_height_and_bal_factor(right)
        return
        
    def _right_rotate(self, node:Node):
        left = node.left
        # left child's right child becomes node's new left child
        node.left = left.right
        if node.left.value:
            node.left.parent = node
        # node's parent becomes left child's new parent
        if not node.parent:
            self.root = left
        elif node.parent.left == node:
            node.parent.left = left
        else:
            node.parent.right = left 
        left.parent = node.parent
        # node becomes left child's new right child
        left.right = node
        node.parent = left
        # fix height and bal_factor
        self._update_height_and_bal_factor(node)
        self._update_height_and_bal_factor(left)
        return
    
    def _update_height_and_bal_factor(self, node: Node):
        node.height = max(node.left.height, node.right.height) + 1
        node.bal_factor = node.left.height - node.right.height
        return
    
    def _transplant(self, dest: Node, source: Node):
        if not dest.parent:
            self.root = source
        elif dest.parent.left == dest:
            dest.parent.left = source
        else:
            dest.parent.right = source
        if source.value:
            source.parent = dest.parent
        return

# Trees
''' tree1
        15
       /   \
     10     25
    /   \     \
   2     13     40
'''    
tree1 = Node(value=15)
tree1.left = Node(value=10, parent=tree1)
tree1.right = Node(value=25, parent=tree1)
tree1.left.left = Node(value=2, parent=tree1.left)
tree1.left.right = Node(value=13, parent=tree1.left)
tree1.right.right = Node(value=40, parent=tree1.right)

''' tree2
        15
          \
            25
              \
                40
'''
tree2 = Node(value=15)
tree2.right = Node(value=25, parent=tree2)
tree2.right.right = Node(value=40, parent=tree2.right)

''' tree3
           15
          /   \
         10    25
                 \
                  40
'''
tree3 = Node(value=15)
tree3.left = Node(value=10, parent=tree3)
tree3.right = Node(value=25, parent=tree3)
tree3.right.right = Node(value=40, parent=tree3.right)

''' tree4
           15
          /   \
         10    25
              /   
            20
'''
tree4= Node(value=15)
tree4.left = Node(value=10, parent=tree4)
tree4.right = Node(value=25, parent=tree4)
tree4.right.left = Node(value=20, parent=tree4.right)

'''
test_insert
        15                                 15                               15
       /   \                             /    \                           /    \
     10     25                          10     25                        10     25
    /   \     \          ->            /   \     \                      /   \     \
   2     13     40                    2    13    40                    2    13    40
          /                                /                               /  \
        12                                14                              12   14
         \                               /
          14                            12
'''

'''
test_delete4
        15                          15
      /   \                        /   \
     10    25                    12     25
    /   \    \       ->         /  \     \
   2    13    40               2    13    40
        /  \                          \
       12   14                         14
'''

class TestAvlTree(unittest.TestCase):
    
    def setUp(self):
        self.tree = copy.deepcopy(tree1)
        self.avl = AvlTree(self.tree)

    def test_validate(self):
        avl = self.avl
        self.assertRaises(ValueError, AvlTree, copy.deepcopy(tree2))
    
    def test_search(self):
        avl = self.avl
        self.assertEqual(avl.search(2), avl.root.left.left)
        self.assertEqual(avl.search(20), None)
    
    def test_find_max(self):
        avl = self.avl
        self.assertEqual(avl.find_max(avl.root), avl.root.right.right)
    
    def test_find_min(self):
        avl = self.avl
        self.assertEqual(avl.find_min(avl.root), avl.root.left.left)
    
    def test_find_successor(self):
        avl = self.avl
        self.assertEqual(avl.find_successor(avl.root), avl.root.right)
        self.assertEqual(avl.find_successor(avl.root.left.right), avl.root)
        self.assertEqual(avl.find_successor(avl.root.left.left), avl.root.left)
        self.assertEqual(avl.find_successor(avl.root.right.right), None)
    
    def test_find_predecessor(self):
        avl = self.avl
        self.assertEqual(avl.find_predecessor(avl.root), avl.root.left.right)
        self.assertEqual(avl.find_predecessor(avl.root.left.left), None)
        self.assertEqual(avl.find_predecessor(avl.root.right.right), avl.root.right)
    
    def test_insert(self):
        avl = self.avl
        avl.insert(Node(value=12))
        avl.insert(Node(value=14))
        self.assertEqual(avl.root.left.right.left.value, 12)
        self.assertEqual(avl.root.left.right.right.value, 14)
        # AvlTree.dfs_in_order(avl.root, True)
    
    def test_delete1(self):
        tree = copy.deepcopy(tree2)
        tree.left = Node(value=10, parent=tree)
        avl = AvlTree(tree)
        avl.delete(avl.root.left)
        self.assertEqual(avl.root.value, 25)
        self.assertEqual(avl.root.left.value, 15)
        self.assertEqual(avl.root.right.value, 40)
        # AvlTree.dfs_in_order(avl.root, True)
    
    def test_delete2(self):
        tree = copy.deepcopy(tree3)
        avl = AvlTree(tree)
        avl.delete(avl.root.right)
        self.assertEqual(avl.root.right.value, 40)
        # AvlTree.dfs_in_order(avl.root, True)
    
    def test_delete3(self):
        tree = copy.deepcopy(tree4)
        avl = AvlTree(tree)
        avl.delete(avl.root.right)
        self.assertEqual(avl.root.right.value, 20)
        # AvlTree.dfs_in_order(avl.root, True)

    def test_delete4(self):
        avl = self.avl
        avl.insert(Node(value=12))
        avl.insert(Node(value=14))
        avl.delete(avl.root.left)
        self.assertEqual(avl.root.left.value, 12)
        self.assertEqual(avl.root.left.right.value, 13)
        # AvlTree.dfs_in_order(avl.root, True)
    
    def test_delete5(self):
        avl = self.avl
        avl.delete(avl.root)
        self.assertEqual(avl.root.value, 25)
        self.assertEqual(avl.root.left.value, 10)
        # AvlTree.dfs_in_order(avl.root, True)
        
if __name__ == '__main__':
    unittest.main()
