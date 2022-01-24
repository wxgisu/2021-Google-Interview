import operator
from os import access
import sys
sys.path.append("/Users/Xiaoguang/Study/CS/Interviews/2021-Google")

from operator import itemgetter
from data_structure.src.disjoint_set import DisjointSet
import unittest
import heapq

def kruskal(graph):
    """
    graph: List[List[Tuple[int, int]]]  aka [ [(node_id, weight), ...], ... ]
    return: mst: List[Tuple[int, int, int]], mst_len: int
    """
    if graph == None or len(graph) == 0:
        raise ValueError

    mst = []
    mst_len = 0
    
    nodes = range(len(graph))
    ds = DisjointSet()
    for node in nodes:
        ds.make_set(node)
    num_set = len(nodes)
    edges = sorted(_get_edges(graph), key=itemgetter(2)) # ElogE
    
    for from_node, to_node, weight in edges: # E
        if ds.find(from_node) != ds.find(to_node): # logV
            ds.union(from_node, to_node)
            num_set -= 1
            mst.append([from_node, to_node, weight])
            mst_len += weight
    
    if num_set != 1:
        raise Exception("Graph is disconnected")
    
    return mst, mst_len

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
    if graph == None or len(graph) == 0:
        raise ValueError

    mst = []
    mst_len = 0
    
    start = 0
    frontier = [(0, start, None)]
    done = set()
    
    while frontier and len(done) != len(graph): # O(V)
        node_weight, node, node_parent = heapq.heappop(frontier) # O(logE)
        if node in done:
            continue
        mst.append((node_parent, node, node_weight))
        mst_len += node_weight
        done.add(node)
        for neighbor, weight in graph[node]:
            if neighbor not in done:
                heapq.heappush(frontier, (weight, neighbor, node)) # O(logE)
    
    if len(done) != len(graph):
        raise Exception("Graph is disconnected")
    
    return mst[1:], mst_len

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
    
