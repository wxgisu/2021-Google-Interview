from typing import List, Set
from collections import deque

def dfs(graph):
    """
    This is the outter loop of the basic recursive version of DFS
    It returns the topological order of nodes as output. 
    This function is equivilent to topological sort
    """
    validate(graph)
    nodes_in_topo_order = deque([])
    seen = set()

    for node in range(len(graph)):
        if node not in seen:
            dfs_visit(graph, node, seen, nodes_in_topo_order)

    return list(nodes_in_topo_order)

def dfs_visit(graph, node, seen, nodes_in_topo_order):
    """
    This is the basic recursive version of DFS
    It uses a set to track discovered nodes, i.e. when nodes are FIRST seen
    It uses a double ended queue to populate nodes in topological order during DFS
    """
    seen.add(node)
    for neighbor in graph[node]:
        if neighbor not in seen:
            dfs_visit(graph, neighbor, seen, nodes_in_topo_order)
    nodes_in_topo_order.appendleft(node)
    return

"""
    0 -> 1 -> 2 -> 4 -> 3
                ↓    
                5
                
    ---dfs---
    nodes_in_topo_order = [0, 1, 2, 5, 4, 3]
    seen = {0, 1, 2, 4, 3, 5}
    node = 5
    dfs_visit(graph, 0, seen, nodes_in_topo_order)

    ---dfs_visit---
        dfs_visit(graph, 1, seen, nodes_in_topo_order)
            dfs_visit(graph, 2, seen, nodes_in_topo_order)
                dfs_visit(graph, 4, seen, nodes_in_topo_order)
                    dfs_visit(graph, 3, seen, nodes_in_topo_order)
                    <-
                <-
                dfs_visit(graph, 5, seen, nodes_in_topo_order)
                <-
            <-
        <-
    <-
"""
    
def strongly_connected_components(graph):
    """
    This returns the strongly connecte components of a directed graph in a list of list.
    1. topological sort
    2. build reverse graph
    2. dfs traverse reverse graph in topo order
    """
    validate(graph)
    nodes_in_topo_order = dfs(graph)
    reverse_graph = build_reverse_graph(graph)
    print(reverse_graph)
    return get_strongly_connected_components(reverse_graph, nodes_in_topo_order)

def build_reverse_graph(graph: List[List[int]]):
    nodes = range(len(graph))
    reverse_graph = [[] for i in nodes]
    
    for from_node in nodes:
        for to_node in graph[from_node]:
            reverse_graph[to_node].append(from_node)

    return reverse_graph

def get_strongly_connected_components(graph, nodes):
    scc_list = []
    seen = set()
    component = []
    for node in nodes:
        if node not in seen:
            dfs_visit_scc(graph, node, seen, component)
            scc_list.append(component.copy())
            component.clear()
    return scc_list

def dfs_visit_scc(graph, node, seen, scc):
    seen.add(node)
    scc.append(node)
    for neighbor in graph[node]:
        if neighbor not in seen:
            dfs_visit_scc(graph, neighbor, seen, scc)
    return

"""
    0 -> 1      5
    ↑    ↓     ↗  ↘
    3 <- 2 -> 4 <- 6 -> 7

        graph2 = [
            [1],
            [2],
            [3, 4],
            [0],
            [5],
            [6],
            [4, 7],
            []

    ---strongly_connected_component---
    nodes_in_topo_order = [0, 1, 2, 4, 5, 6, 7, 3]
    reverse_graph = [
            [3], #0
            [0], #1
            [1], #2
            [2], #3
            [2, 6], #4
            [4], #5
            [5], #6
            [6], #7
    ]

    0 <- 1      5
    ↓    ↑     ↙  ↖
    3 -> 2 <- 4 -> 6 <- 7

    ---get_strongly_connected_components---
    scc_list = []
    seen = {}
    component = []
    node = 
    dfs_visit_scc(graph, , seen, [])

    ---dfs_visit_scc---

"""
            
def has_cycle(graph):
    """
    Takes a graph as input, returns boolean representing is there is any cycle in the graph
    """
    validate(graph)
    seen = set()
    result = False
    for node in range(len(graph)):
        if node not in seen:
            visiting = set()
            result = result or dfs_has_cycle(graph, node, seen, visiting)
    return result

def dfs_has_cycle(graph, node, seen, visiting): # 
    """
    This is the dfs visit part for cycle detection
    """
    seen.add(node)
    visiting.add(node)
    
    for neighbor in graph[node]:
        if neighbor in visiting:
            return True
        if neighbor not in seen:
            if dfs_has_cycle(graph, neighbor, seen, visiting):
                return True
    
    visiting.remove(node)
    return False

"""
    0 -> 1 -> 2
        ↑    ↓
        3 ←  4   

    ---has_cycle---
    seen = {0, 1, 2, 4, 3}
    result = True
    node = 3
    visiting = {0, 1, 2, 4, 3}
    dfs_has_cycle(graph, 0, {}, {})

    ---dfs_has_cycle---
        dfs_has_cycle(graph, 1, seen, visiting)
            dfs_has_cycle(graph, 2, seen, visiting)
                dfs_has_cycle(graph, 4, seen, visiting)
                    dfs_has_cycle(graph, 3, seen, visiting)
                    <-True
                <-True
            <-True
        <-True
    <-True        
"""

def dfs_iterative(graph):
    """
    The outter loop for iterative version of dfs. It returns a list of nodes in topological order.
    """
    validate(graph)
    nodes_in_topo_order = deque([])
    seen = set()
    for node in range(len(graph)):
        if node not in seen:
            dfs_visit_iterative(graph, node, seen, nodes_in_topo_order)
    return list(nodes_in_topo_order)
        
def dfs_visit_iterative(graph, start, seen, nodes_in_topo_order):
    """
    The iterative version of dfs visit. It returns a list of nodes that are reachable from start in topological order.
    """
    frontier = [(start, None)]
    parent = []
    seen.add(start)
    
    while frontier or parent:
        if not frontier:
            nodes_in_topo_order.appendleft(parent.pop()[0])
        elif not parent or frontier[-1][1] == parent[-1][0]:
            node, node_parent= frontier.pop()
            parent.append((node, node_parent))
            for neighbor in graph[node]:
                if neighbor not in seen:
                    frontier.append((neighbor, node))
                    seen.add(neighbor)
        else:
            nodes_in_topo_order.appendleft(parent.pop()[0])
    return

"""
    0 -> 1 -> 2 -> 4 -> 3
                ↓    
                5
                
    frontier = [ ]
    parent = [  ]
    seen = {0, 1, 2, 4, 5}
    result = [(5, 2), (4, 2), (2, 1), (1, 0), (0, None)]
    result.reverse()

    node = (4, 2)
"""

def validate(graph):
    if graph == None:
        raise ValueError
    return
    
def main():
    '''
        0 -> 1 -> 2 -> 4 -> 3
                  ↓    
                  5 
    '''
    graph1 = [
        [1], # 0
        [2], # 1
        [4, 5], # 2
        [], # 3
        [3], # 4
        [], # 5
    ]
    
    '''
        0 -> 1      5
        ↑    ↓     ↗  ↘
        3 <- 2 -> 4 <- 6 -> 7
    '''
    graph2 = [
        [1],
        [2],
        [3, 4],
        [0],
        [5],
        [6],
        [4, 7],
        []
    ]
    
    '''
        0 -> 1 -> 2 -> 3 -> 5 -> 7
                     ↘   ↗
                       4 -> 6 -> 8
    '''
    graph3 = [
        [1],
        [2], 
        [3, 4],
        [5],
        [5, 6],
        [7],
        [8],
        [],
        []
    ]
    
    '''
    0 -> 1 -> 2
         ↑    ↓
         3 ←  4   
    '''
         
    graph4 = [
        [1],
        [2],
        [4],
        [1],
        [3],
    ]

    t1_dfs = (dfs(graph1), [0, 1, 2, 5, 4, 3])
    t1_scc = (strongly_connected_components(graph1), [[0], [1], [2], [5], [4], [3]])
    t1_cycle = (has_cycle(graph1), False)
    t1_dfs_iter = (dfs_iterative(graph1), [0, 1, 2, 4, 3, 5])
    
    t2_dfs = (dfs(graph2), [0, 1, 2, 4, 5, 6, 7, 3])
    t2_scc = (strongly_connected_components(graph2), [[0, 3, 2, 1], [4, 6, 5], [7]])
    t2_cycle = (has_cycle(graph2), True)
    
    t3_dfs = (dfs(graph3), [0, 1, 2, 4, 6, 8, 3, 5, 7])
    t3_scc = (strongly_connected_components(graph3), [[0], [1], [2], [4], [6], [8], [3], [5], [7]])
    t3_cycle = (has_cycle(graph3), False)
    
    t4_dfs = (dfs(graph4), [0, 1, 2, 4, 3])
    t4_scc = (strongly_connected_components(graph4), [[0], [1, 3, 4, 2]])
    t4_cycle = (has_cycle(graph4), True)
    
    tests = {
        't1_dfs': t1_dfs,
        't1_scc': t1_scc,
        't1_cycle': t1_cycle,
        't1_dfs_iter': t1_dfs_iter,
        't2_dfs': t2_dfs,
        't2_scc': t2_scc,
        't2_cycle': t2_cycle,
        't3_dfs': t3_dfs,
        't3_scc': t3_scc,
        't3_cycle': t3_cycle,
        't4_dfs': t4_dfs,
        't4_scc': t4_scc,
        't4_cycle': t4_cycle,
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

if __name__ == '__main__':
    main()