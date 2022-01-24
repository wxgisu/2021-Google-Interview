import heapq
from dataclasses import dataclass
from typing import Optional
from copy import copy
import unittest

def dijkstra(graph, source):
    """
    graph: List[List[Tuple[int, int]]] [ [(node, weight), ...], [...], ... ]
    source: int
    
    Node is represented as a Tuple 
    (distance, id, parent_id)
    
    This implementation don't collect all nodes in advance, then update each node during the bfs process. 
    Instead, it allows nodes to be added into the frontier more than once, i.e. it allows any node to be 
    discovered via all incoming edges. Since the while loop stops when number of nodes in finished is equal to 
    total number of nodes (V), the run time is O(VlgE + ElgE) when using a binary heap. 
    The space complexity is O(E) since node via each edge can be enqueued into the frontier.
    """
    result = [] # this is only used for testing purpose, not part of the algo
    nodes = range(len(graph))
    frontier = [(0, source, None)] # data: (distance, node, parent)
    distance = {node: float('inf') for node in nodes}
    done = set()
    while frontier and len(done) < len(nodes):
        node_dist, node, node_parent = heapq.heappop(frontier)
        if node in done:
            continue
        done.add(node)
        distance[node] = node_dist
        result.append((node, node_dist, node_parent))
        for neighbor, weight in graph[node]:
            if neighbor not in done:
                heapq.heappush(frontier, (weight+node_dist, neighbor, node))

    return result

@dataclass
class Node:
    id: int
    distance: int = float('inf')
    parent: Optional['Node'] = None
    
    def __lt__(self, other: 'Node'):
        return self.distance < other.distance
    
def dijkstra_with_node_helper_class(graph, source):
    """
    graph: List[List[Tuple[int, int]]]
    source: int
    """
    result = []
    frontier = [Node(source, 0)]
    nodes = {id: None for id in range(len(graph))}
    done = set()

    while frontier and len(done) < len(graph):
        node = heapq.heappop(frontier)
        if node.id in done:
            continue
        nodes[node.id] = node
        result.append(node)
        done.add(node.id)
        for neighbor_id, weight in graph[node.id]:
            if neighbor_id not in done:
                neighbor = Node(neighbor_id, node.distance + weight, node.id)
                heapq.heappush(frontier, neighbor)
    
    paths = []
    for node_id, node in nodes.items():
        path = []
        cur = node_id
        while cur != None:
            path.append(cur)
            cur = nodes[cur].parent
        path.reverse()
        paths.append(path)
    print(paths)

    return result

def bellman_ford(graph, source):
    nodes = range(len(graph))
    distance = {node: float('inf') for node in nodes}
    parent = {node: None for node in nodes}
    distance[source] = 0
    edges = get_edges(graph)

    for i in range(len(graph)-1):
        for from_node, to_node, weight in edges:
            new_distance = distance[from_node] + weight
            if new_distance < distance[to_node]:
                distance[to_node] = new_distance
                parent[to_node] = from_node
    
    for from_node, to_node, weight in edges:
        new_distance = distance[from_node] + weight
        if new_distance < distance[to_node]:
            raise Exception("There is negative cycle in graph")
    
    return distance

def get_edges(graph):
    edges = []
        
    for from_node in range(len(graph)):
        for to_node, weight in graph[from_node]:
            edges.append((from_node, to_node, weight))
    
    return edges

# Graphs
'''
    0 -> 1  -> 2
         ↓     ↑
         3  -> 4
'''
graph1 = [
    [(1, 5)],
    [(2, 10), (3, 5)],
    [],
    [(4, 1)],
    [(2, 1)]
]

'''
    0 -> 1 -> 2
          ↖  ↙
            3
'''
graph2 = [
    [(1, 5)],
    [(2, 1)],
    [(3, -5)],
    [(1, 1)]
]

def main():
    t1_dijkstra = dijkstra(graph1, 0)
    t1_dijkstra_res = [(0, 0, None), (1, 5, 0), (3, 10, 1), (4, 11, 3), (2, 12, 4)]

    t1_dijkstra_with_node_helper = dijkstra_with_node_helper_class(graph1, 0)
    t1_dijkstra_with_node_helper_res = [
        Node(0, 0, None), 
        Node(1, 5, 0),
        Node(3, 10, 1),
        Node(4, 11, 3),
        Node(2, 12, 4),
    ]
    
    t1_bellmen_ford = bellman_ford(graph1, 0)
    t1_bellmen_ford_res = {0: 0, 1: 5, 2: 12, 3: 10, 4: 11}
    
    tests = {
        't1_dijkstra': (t1_dijkstra, t1_dijkstra_res),
        't1_dijkstra_with_node_helper': (t1_dijkstra_with_node_helper, t1_dijkstra_with_node_helper_res),
        't1_bellmen_ford': (t1_bellmen_ford, t1_bellmen_ford_res),
    }
    
    for test_name, test_data in tests.items():
        actual = test_data[0]
        expected = test_data[1]
        try:
            assert(actual == expected)
            print(f'{test_name} succeed')
        except:
            print(f'{test_name} failed')
            print(f'Expected {expected}, but actual was {actual}')
            
class TestBellmenFord(unittest.TestCase):
    def test_negative_cycle(self):
        self.assertRaises(Exception, bellman_ford, graph2, 0)

if __name__ == '__main__':
    main()
    unittest.main()
    