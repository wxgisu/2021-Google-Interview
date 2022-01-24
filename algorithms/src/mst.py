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
    mst = []
    mst_len = 0
    if len(graph) == 0:
        raise ValueError
    if len(graph) == 1:
        return mst, mst_len

    nodes = [i for i in range(len(graph))]
    ds = DisjointSet()
    for node in nodes:
        ds.make_set(node)
    set_num = len(nodes)
    
    edges = _get_edges(graph) # (from_node, to_node , weight)
    edges.sort(key=itemgetter(2))

    for from_node, to_node, weight in edges:
        if ds.find(from_node) != ds.find(to_node):
            ds.union(from_node, to_node)
            set_num -= 1
            mst.append((from_node, to_node, weight))
            mst_len += weight
    
    if set_num > 1:
        raise ValueError("The input graph is disconnected and therefore can't find any MST")
    
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
    if not graph:
        raise ValueError
    if len(graph) == 0:
        return [], 0
    
    mst = []
    mst_len = 0
    frontier = [(0, 0, None)] # [ (10, 2, 1) ]
    finished = set()

    while len(mst) != len(graph) and frontier:
        weight, node, parent = heapq.heappop(frontier) # 5, 4, 3
        if node in finished:
            continue
        finished.add(node) # {0, 1, 3, 2, 4}
        mst.append((parent, node, weight)) # [ (None, 0, 0), (0, 1, 5), (1, 3, 5), (3, 2, 5), (3, 4, 5)]
        mst_len += weight # 20
        for neighbor, weight in graph[node]: # 3, 5
            if neighbor in finished:
                continue
            heapq.heappush(frontier, (weight, neighbor, node))
    
    if len(mst) != len(graph):
        raise Exception("Graph is not connected")
    mst.pop(0)
    return mst, mst_len


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
    
