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
    total number of nodes (V), the run time is O(VlgV + ElgE) when using a binary heap. 
    The space complexity is O(E) since node via each edge can be enqueued into the frontier.
    """
    shortest_paths = []
    frontier = [(0, source, None)]
    finished = set()
    
    while len(finished) != len(graph):
        distance, node, parent  = heapq.heappop(frontier)
        if node in finished:
            continue
        finished.add(node)
        shortest_paths.append((node, distance, parent))
        for neighbor, weight in graph[node]:
            if neighbor not in finished:
                heapq.heappush(frontier, (distance + weight, neighbor, node))
    
    return shortest_paths

@dataclass
class Node:
    id: int
    distance: int = float('inf')
    parent: Optional[int]  = None
    
    def __lt__(self, other: 'Node'):
        return self.distance < other.distance
    
def dijkstra_with_node_helper_class(graph, source):
    """
    graph: List[List[Tuple[int, int]]]
    source: Node
    """
    nodes = []
    source_node = Node(source, 0)
    frontier = [source_node]
    finished = set()
    
    while len(finished) != len(graph):
        node = heapq.heappop(frontier)
        if node.id in finished:
            continue 
        finished.add(node.id)
        nodes.append(node)
        for neighbor_id, weight in graph[node.id]:
            if neighbor_id not in finished:
                new_distance = node.distance + weight
                neighbor = Node(neighbor_id, new_distance, node.id)
                heapq.heappush(frontier, neighbor)
    
    return nodes
    
def dijkstra_no_repeat_with_node_helper_class(graph, source):
    
    """
    graph: List[List[Tuple[int, int]]]
    soruce: Node
    
    This is the same inplementation as in the CLRS text book. In this implementation, all the nodes are added to the
    priority queue at the beginning, and never enqued again. Then it takes V steps to extract the min out of the 
    priority queue. So the run time for this with a binary heap is O(VlgV + ElgV). This is better than the version 
    that allows repeated nodes in the priority queue. The space complexity O(V) is also better. But this implementation
    requires to access the DECREASE_KEY operation of the priority queue. See below for detailed explanation.
    """
    nodes = [Node(i) for i in range(len(graph))]
    nodes[source].distance = 0
    frontier = copy(nodes)
    heapq.heapify(frontier)
    
    while frontier:
        node = heapq.heappop(frontier)
        for neighbor_id, weight in graph[node.id]:
            neighbor = nodes[neighbor_id]
            if neighbor.distance > node.distance + weight:
                neighbor.distance = node.distance + weight
                neighbor.parent = node.id
                '''
                Here needs the DECREASE_KEY operation in the heapq, but also needs to dynamically update
                the heapq position for every element whose positiion is changed during the DECREASE_KEY op.
                This requires a dictionary maps from heapq element to position with in the heapq, and gets update
                when the _shiftup() method (aka the DECREASE_KEY operation in the python heapq) is called. The current
                python version of heapq doesn't support sunch dictionary. 
                '''
                # heapq._siftup() 
    pass

def bellman_ford(graph, source):
    nodes = [i for i in range(len(graph))]
    distance = {node: float('inf') for node in nodes}
    parent = {node: None for node in nodes}
    distance[source] = 0
    
    for i in range(len(nodes) - 1):
        for from_node, to_node, weight in _get_edges(graph):
            new_distance = distance[from_node] + weight
            if new_distance < distance[to_node]:
                distance[to_node] = new_distance
                parent[to_node] = from_node
                
    for from_node, to_node, weight in _get_edges(graph):
        new_distance = distance[from_node] + weight
        if new_distance < distance[to_node]:
            raise ValueError("The input graph has negative cycle")
            
    return distance

def _get_edges(graph):
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
        self.assertRaises(ValueError, bellman_ford, graph2, 0)

if __name__ == '__main__':
    main()
    unittest.main()
    