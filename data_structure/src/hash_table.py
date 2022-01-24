from typing import Any
from dataclasses import dataclass
import unittest

@dataclass
class Node:
    key: Any
    value: Any

class HashTable:

    def __init__(self):
        self.size = 1000
        self.hash_table = [None] * self.size
        pass

    def get(self, key: Any) -> Any:
        index = self._hash(key)
        node = self.hash_table[index]
        if not node:
            return node
        elif type(node) is list:
            return self._find_key(index, key)
        else:
            return node.value

    def put(self, key: Any, val: Any):
        index = self._hash(key)
        node = self.hash_table[index]
        new_node = Node(key, val)
        if not node: # no collision
            self.hash_table[index] = new_node
        elif type(node) is not list: # first collision
            if node.key == key:
                node.value = val
            else:
                node = [node, new_node]
        else: # non-first collision
            self._set_key(index, key, val)
        return
    
    def _hash(self, key: Any) -> int:
        return hash(key) % self.size
    
    def _find_key(self, index, target_key):
        for node in self.hash_table[index]:
            if node.key == target_key:
                return node.value
        return None
    
    def _set_key(self, index, key, val):
        nodes = self.hash_table[index]
        for node in nodes:
            if node.key == key:
                node.value = val
                return
        nodes.append(Node(key, val))

class TestHashTable(unittest.TestCase):
    
    def setUp(self):
       self.ht = HashTable()
    
    def test_put(self):
        ht = self.ht
        ht.put("hello", "world")
        index = ht._hash("hello")
        self.assertEqual("hello", ht.hash_table[index].key)
        self.assertEqual("world", ht.hash_table[index].value)
        ht.put("hello", "again")
        self.assertEqual("again", ht.hash_table[index].value)
    
    def test_get(self):
        ht = self.ht
        ht.put("hello", "world")
        self.assertEqual("world", ht.get("hello"))
        self.assertEqual(None, ht.get("random"))

if __name__ == '__main__':
    unittest.main()