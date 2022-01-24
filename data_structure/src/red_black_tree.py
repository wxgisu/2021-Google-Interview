from dataclasses import dataclass
from typing import Optional
import unittest
import copy


BLACK = 'black'
RED = 'red'

@dataclass
class Node:
    color: str
    value: Optional[int] = None
    parent: Optional['Node'] = None
    left: Optional['Node'] = None
    right: Optional['Node'] = None
    
class RedBlackTree():
    """
    red-black tree properties:
    1. every node is either red or black
    2. root and leaf nodes are black
    3. there's no red-red parent child relationship
    4. all root to leaf simple paths contains same number of black nodes
    """
    def __init__(self, root: Node):
        self.root = copy.deepcopy(root)
        self.validate()

    @staticmethod
    def dfs_in_order(node: Node, verbose=False):
        result = []
        stack = []
        current = node
        while stack or current:
            if current:
                stack.append(current)
                current = current.left
            else:
                current = stack.pop()
                result.append(current.value)
                if verbose:
                    print(current.value, current.color)
                current = current.right
        return result
    
    def validate(self):
        root = self.root
        stack = [] #
        current = (root, float('-inf'), float('inf'))
        while stack or current[0]:
            if current[0]:
                node, lower, upper = current 
                if node.value < lower or node.value > upper: 
                    raise ValueError("Input tree is not a binary search tree")
                if node.right: 
                    stack.append((node.right, node.value, upper))
                current = (node.left, lower, node.value)
            else:
                current = stack.pop()
        return
    
    def find_min(self, node: Node):
        current = node
        while current and current.left:
            current = current.left
        return current
    
    def find_successor(self, node: Node) -> Optional[Node]:
        if node == None:
            return None
        if node.right:
            return self.find_min(node.right)
        parent = node.parent
        current = node
        while parent and parent.right == current:
            current, parent = parent, parent.parent
        return parent

    def left_rotate(self, node: Node):
        """
              p                    p                      ----→ p                      p
              ↓↑                   ↓↑                     |    ↑↓                     ↑↓
             node                 node                    |   right                  right
             ↙↗ ↘↖       ->      ↙↗ |↑  ↖         ->      |     | ↖↘       ->       ↙↗    ↘↖
            a   right           a   ||  right            node   |    c            node      c
                ↙↗  ↘↖               ↘\  ↙  ↖↘          ↙↗ ↖↘  ↙                  ↙↗ ↖↘
               b      c                b      c        a     b                   a     b      

                    fix node.right        fix right.parent          fix right.left
        """
        right = node.right
        if not right:
            print("No need to left rotate since node.right doesn't exist")
            return
        # move right's left subtree to node's right subtree
        node.right = right.left
        if right.left:
            right.left.parent = node
        # change node's parent to become right's parent
        right.parent = node.parent
        if not node.parent:
            self.root = right
        elif node.parent.left == node:
            node.parent.left = right
        else:
            node.parent.right = right
        # move node to right's left subtree
        right.left = node
        node.parent = right
        return 

    def right_rotate(self, node: Node):
        """
                  p                    p                    p ←---                  p
                  ↓↑                   ↓↑                   ↓↑   |                  ↓↑
                 node                 node                 left  |                 left
                ↙↗  ↘↖       ->      ↗ ↑| ↘↖      ->      ↙↗ |   |        ->      ↙↗  ↘↖
              left    c           left ||   c            a   |  node             a     node
             ↙↗  ↘↖              ↙↗  ↘ /↙                     ↘ ↙↗ ↘↖                  ↙↗ ↘↖
            a      b            a     b                        b    c                 b     c

                       fix node.left           fix left.parent         fix left.right     
        """
        left = node.left
        if not left:
            print("No need to right rotate since node.left doesn't exist")
            return
        # move left's right subtree to node's left subtree
        node.left = left.right
        if left.right:
            left.right.parent = node
        # change node's parent to become left's parent
        left.parent = node.parent
        if not node.parent:
            self.root = left
        elif node.parent.left == node:
            node.parent.left = left
        else:
            node.parent.right = left
        # move node to left's right subtree
        left.right = node
        node.parent = left
        return

    def insert(self, node: Node):
        parent = None
        current = self.root
        # walk to find where to insert node
        while current:
            parent = current
            if node.value < current.value:
                current = current.left
            else:
                current = current.right
        # set node's parent and parent's child pointer
        node.parent = parent
        if parent == None:
            self.root = node
        elif node.value < parent.value:
            parent.left = node
        else:
            parent.right = node
        # set node's color and fix violated red-black properties
        node.color = RED
        node.left = node.right = None
        self._insert_fixup(node)
        return
    
    def _insert_fixup(self, node: Node):
        while node.parent and node.parent.color == RED:
            parent = node.parent
            # if parent exist, node must not be root, and root must still be BLACK
            # since parent is RED, it must not be root neither, which means parent's parent must exist
            if parent == parent.parent.left:
                uncle = parent.parent.right
                if uncle and uncle.color == RED: # case 1
                    parent.color = uncle.color = BLACK
                    parent.parent.color = RED
                    node = parent.parent
                else:
                    if node == parent.right: # case 2
                        node = parent
                        self.left_rotate(node) # transform to case 3
                        parent = node.parent
                    parent.color = BLACK # case 3
                    parent.parent.color = RED
                    self.right_rotate(parent.parent) 
            else:
                uncle = parent.parent.left
                if uncle and uncle.color == RED: # case 1
                    parent.color = uncle.color = BLACK
                    parent.parent.color = RED
                    node = parent.parent
                else:
                    if node == parent.left: # case 2
                        node = parent 
                        self.right_rotate(node) # transform into case 3
                        parent = node.parent
                    parent.color = BLACK # case 3
                    parent.parent.color = RED
                    self.left_rotate(parent.parent)
        self.root.color = BLACK
        return 
    
    def delete(self, node: Node):
        node_to_be_removed_color = node.color
        if not node.left:
            node_to_replace_removed = node.right
            self._transplant(node, node.right)
        elif not node.right:
            node_to_replace_removed = node.left
            self._transplant(node, node.left)
        else:
            successor = self.find_successor(node)
            node_to_be_removed_color = successor.color
            node_to_replace_removed = successor.right
            if node.right != successor:
                self._transplant(successor, successor.right)
                successor.right = node.right
                successor.right.parent = successor
            self._transplant(node, successor)
            successor.left = node.left
            successor.left.parent = successor
        if node_to_be_removed_color == BLACK and node_to_replace_removed:
            self._delete_fixup(node_to_replace_removed)
        return
    
    def _transplant(self, dest: Node, source: Node):
        # change parent -> child pointer
        if dest.parent == None:
            self.root = source
        elif dest == dest.parent.left:
            dest.parent.left = source
        else:
            dest.parent.right = source
        # change child -> parent pointer
        if source:
            source.parent = dest.parent
        return

    def _delete_fixup(self, node: Node):
        """
        case 1: node's sibling is red -> recolor sibling and parent, rotate parent
        case 2: node's sibling is black, sibling's left and right child are black -> color sibling to red, update node to node's parent
        case 3: node's sibling is black, sibling's left is red, right is black -> recolor sibling's left and sibling, rotate sibling
        case 4: node's sibling is black, sibling's right is red -> set sibling to parent's color, set parent and siblin'g right to black, rotate parent [end case]
        """
        while node != self.root and node.color == BLACK:
            parent = node.parent
            if node == parent.left:
                sibling = parent.right
                if sibling.color == RED: # case 1
                    # sibling's parent and children must all be BLACK
                    sibling.color = BLACK
                    parent.color = RED
                    self.left_rotate(parent) # transform to case 2 or 3 or 4
                    sibling = parent.right # this is left child of sibling before rotation
                if ( (not sibling.left or sibling.left.color == BLACK) 
                    and (not sibling.right or sibling.right.color == BLACK) ): # case 2
                    sibling.color = RED
                    node = parent
                    continue
                elif ( (sibling.left and sibling.left.color == RED)
                    and (not sibling.right or sibling.right.color == BLACK) ): # case 3
                    sibling.left.color = BLACK
                    sibling.color = RED
                    self.right_rotate(sibling) # transform to case 4
                    sibling = node.parent.right
                sibling.color = parent.color # case 4
                sibling.right.color = BLACK
                parent.color = BLACK
                self.left_rotate(parent)
                node = self.root
            else:
                sibling = node.parent.left
                if sibling.color == RED: # case 1
                    sibling.color = BLACK
                    parent.color = RED
                    self.right_rotate(parent)
                    sibling = node.parent.left
                if ( (not sibling.right or sibling.right.color == BLACK)
                    and (not sibling.left or sibling.left.color == BLACK) ): # case 2
                    sibling.color = RED
                    node = parent
                    continue
                elif ( (sibling.right and sibling.right.color == RED)
                    and (not sibling.left or sibling.left.color == BLACK) ): # case 3
                    sibling.right.color = BLACK
                    sibling.color = RED
                    self.left_rotate(sibling)
                    sibling = node.parent.left
                sibling.color = parent.color
                sibling.left.color = BLACK
                parent.color = BLACK
                self.right_rotate(parent)
                node = self.root
        node.color = BLACK
        return

# Trees
'''
        9B
      /    \
     5R    15R
   /  \    /  \
  2B   7B 12B  19B
'''
tree1 = Node(BLACK, value=9)
tree1.left = Node(RED, value=5, parent=tree1)
tree1.right = Node(RED, value=15, parent=tree1)
tree1.left.left = Node(BLACK, value=2, parent=tree1.left)
tree1.left.right = Node(BLACK, value=7, parent=tree1.left)
tree1.right.left = Node(BLACK, value=12, parent=tree1.right)
tree1.right.right = Node(BLACK, value=19, parent=tree1.right)

'''
         9B
      /       \
     5B       15R
       \      /  \
       7B    12B  19B
             /     \
           11B     25B
'''
tree2 = Node(BLACK, 9)
tree2.left = Node(BLACK, 5, tree2)
tree2.right = Node(RED, 15, tree2)
tree2.left.right = Node(BLACK, 7, tree2.left)
tree2.right.left = Node(BLACK, 12, tree2.right)
tree2.right.right = Node(BLACK, 19, tree2.right)
tree2.right.left.left = Node(BLACK, 11, tree2.right.left)
tree2.right.right.right = Node(BLACK, 25, tree2.right.right)

class TestRedBlackTree(unittest.TestCase):
    
    def setUp(self):
        self.tree = copy.deepcopy(tree1)
        self.rbt = RedBlackTree(self.tree)

    def test_validate(self):
        self.rbt.validate()
        
    def test_left_rotate(self):
        tree = self.tree
        rbt = self.rbt
        dfs = RedBlackTree.dfs_in_order
        rbt.left_rotate(rbt.root)
        self.assertEqual(rbt.root.value, 15)
        self.assertEqual(rbt.root.right.value, 19)
        self.assertEqual(rbt.root.left.value, 9)
        self.assertEqual(rbt.root.left.right.value, 12)
        self.assertEqual(dfs(rbt.root), dfs(tree))
    
    def test_right_rotate(self):
        tree = self.tree
        rbt = self.rbt
        dfs = RedBlackTree.dfs_in_order
        rbt.right_rotate(rbt.root)
        self.assertEqual(rbt.root.value, 5)
        self.assertEqual(rbt.root.left.value, 2)
        self.assertEqual(rbt.root.right.value, 9)
        self.assertEqual(rbt.root.right.left.value, 7)
        self.assertEqual(rbt.root.right.right.value, 15)
        self.assertEqual(dfs(rbt.root), dfs(tree))
        
    def test_insert(self):
        tree = self.tree
        rbt = self.rbt
        node1 = Node(RED, 3)
        node2 = Node(RED, 4)
        rbt_min_node = rbt.root.left.left
        dfs = RedBlackTree.dfs_in_order
        rbt.insert(node1)
        rbt.insert(node2)
        self.assertEqual(rbt.root.left.left, node1)
        self.assertEqual(rbt.root.left.left.left, rbt_min_node)
        self.assertEqual(rbt.root.left.left.right, node2)
        self.assertEqual(node1.color, BLACK)
        self.assertEqual(node2.color, RED)
        self.assertEqual(rbt_min_node.color, RED)
    
    def test_find_successor(self):
        rbt = self.rbt
        self.assertEqual(rbt.find_successor(rbt.root), rbt.root.right.left)
        self.assertEqual(rbt.find_successor(rbt.root.left.right), rbt.root)
    
    def test_delete(self):
        tree = copy.deepcopy(tree2)
        rbt = RedBlackTree(tree)
        dfs = RedBlackTree.dfs_in_order
        rbt.delete(rbt.root.left)
        self.assertEqual(rbt.root.value, 15)
        self.assertEqual(rbt.root.left.value, 9)
        self.assertEqual(rbt.root.left.left.value, 7)
        self.assertEqual(rbt.root.left.right.value, 12)
        self.assertEqual(rbt.root.left.right.left.value, 11)
        self.assertEqual(rbt.root.right.value, 19)
        self.assertEqual(rbt.root.right.right.value, 25)
        self.assertEqual(rbt.root.color, BLACK)
        self.assertEqual(rbt.root.left.color, BLACK)
        self.assertEqual(rbt.root.left.right.color, RED)

if __name__ == '__main__':
    unittest.main()
