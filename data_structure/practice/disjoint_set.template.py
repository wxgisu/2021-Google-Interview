import unittest

class DisjointSet():
    def __init__(self):
        self.set = {}
    
    def make_set(self, key: int):
        self.set[key] = key
        return
    
    def find(self, key: int):
        parent = self.set[key]
        while self.set[parent] != parent:
            parent = self.set[parent]
        self.set[key] = parent
        return parent
    
    def union(self, key1: int, key2: int):
        parent1 = self.find(key1)
        parent2 = self.find(key2)
        if parent1 != parent2:
            self.set[parent2] = parent1
        return parent1

class TestDisjointSet(unittest.TestCase):
    def test_make_set(self):
        key = 1
        ds = DisjointSet()
        ds.make_set(key)
        self.assertEqual(ds.set[key], key)
        
    def test_find(self):
        ds = DisjointSet()
        ds.make_set(0)
        ds.make_set(1)
        ds.make_set(2)
        ds.make_set(3)
        ds.make_set(4)
        ds.set[1] = 0
        ds.set[2] = 1
        ds.set[4] = 3
        self.assertEqual(ds.find(0), 0)
        self.assertEqual(ds.find(1), 0)
        self.assertEqual(ds.find(2), 0)
        self.assertEqual(ds.find(3), 3)
        self.assertEqual(ds.find(4), 3)
        
    def test_union(self):
        ds = DisjointSet()
        ds.make_set(0)
        ds.make_set(1)
        ds.make_set(2)
        ds.make_set(3)
        ds.make_set(4)
        ds.set[1] = 0
        ds.set[2] = 1
        ds.set[4] = 3
        ds.union(4, 2)
        self.assertEqual(ds.set[0], 3)
        self.assertEqual(ds.set[1], 0)
        self.assertEqual(ds.set[2], 0)
        self.assertEqual(ds.set[3], 3)
        self.assertEqual(ds.set[4], 3)

if __name__ == '__main__':
    unittest.main()


        

    