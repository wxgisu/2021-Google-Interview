import operator
from os import access
import sys
sys.path.append("/Users/Xiaoguang/Study/CS/Interviews/2021-Google")

from operator import itemgetter
from data_structure.disjoint_set import DisjointSet
import unittest
import heapq

def kruskal(graph):
    """
    graph: List[List[Tuple[int, int]]]  aka [ [(node_id, weight), ...], ... ]
    return: mst: List[Tuple[int, int, int]], mst_len: int
    """
    pass

def _get_edges(graph):
    edges = []
    for from_node in range(len(graph)):
        for to_node, weight in graph[from_node]:
            edges.append((from_node, to_node, weight))
    return edges 

def prim(graph):
    """
    graph: List[List[Tuple[int, int]]]  aka [ [(node_id, weight), ...], ... ]
    return: mst: List[Tuple[int, int, int]], mst_len: int
    """
    pass

# Graphs
'''
    0 - 1 - 2 - 3 - 4
        |_______|
'''
graph1 = [
    [(1, 5)],
    [(0, 5), (2, 10), (3, 5)],
    [(1, 10), (3, 5)],
    [(1, 5), (2, 5), (4, 5)],
    [(3, 5)]
]

class Test(unittest.TestCase):
    def test_kruskal_1(self):
        actual = kruskal(graph1)
        expected = ([(0, 1, 5), (1, 3, 5), (2, 3, 5), (3, 4, 5)], 20)
        self.assertEqual(actual, expected)
    
    def test_prim_1(self):
        actual = prim(graph1)
        expected = ([(0, 1, 5), (1, 3, 5), (3, 2, 5), (3, 4, 5)], 20)
        self.assertEqual(actual, expected)

if __name__ == '__main__':
    unittest.main()
    
