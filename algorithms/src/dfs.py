from typing import List, Set
from collections import deque

def dfs(graph):
    """
    This is the outter loop of the basic recursive version of DFS
    It returns the topological order of nodes as output. 
    This function is equivilent to topological sort
    """
    discovered = set()
    nodes_in_topo_order = deque([])
    for node in range(len(graph)):
        if node not in discovered:
            dfs_visit(graph, node, discovered, nodes_in_topo_order)
    return list(nodes_in_topo_order)

def dfs_visit(graph, node, discovered, nodes_in_topo_order):
    """
    This is the basic recursive version of DFS
    It uses a set to track discovered nodes, i.e. when nodes are FIRST seen
    It uses a double ended queue to populate nodes in topological order during DFS
    """
    discovered.add(node)
    for neighbor in graph[node]:
        if neighbor not in discovered:
            discovered.add(neighbor)
            dfs_visit(graph, neighbor, discovered, nodes_in_topo_order)
    nodes_in_topo_order.appendleft(node)
    
def strongly_connected_components(graph):
    nodes_in_topo_order = dfs(graph)
    reverse_graph = build_reverse_graph(graph)
    scc_list = get_strongly_connected_components(reverse_graph, nodes_in_topo_order)
    return scc_list

def build_reverse_graph(graph: List[List[int]]):
    reverse_graph = [ [] for i in range(len(graph))]
    for from_node, to_nodes in enumerate(graph):
        for to_node in to_nodes:
            reverse_graph[to_node].append(from_node)
    return reverse_graph

def get_strongly_connected_components(graph, nodes):
    scc_list = []
    discovered = set()
    for node in nodes:
        if node not in discovered:
            discovered.add(node)
            scc = []
            dfs_visit_scc(graph, node, discovered, scc)
            scc_list.append(scc)
    return scc_list

def dfs_visit_scc(graph, node, discovered, scc):
    scc.append(node)

    for neighbor in graph[node]:
        if neighbor not in discovered:
            discovered.add(neighbor)
            dfs_visit_scc(graph, neighbor, discovered, scc)
            
def has_cycle(graph):
    """
    Takes a graph as input, returns boolean representing is there is any cycle in the graph
    """
    if graph == None:
        return False
    
    discovered = set() # {0, 1, 2, 4, 3} 
    nodes = [i for i in range(len(graph))] # [0, 1, 2, 3, 4]
    for node in nodes: # 0
        if node not in discovered: 
            visiting = set() # {0, 1, 2, 4, 3}
            if dfs_has_cycle(graph, node, discovered, visiting):
                return True
    return False

def dfs_has_cycle(graph, node, discovered, visiting): # 
    """
    This is the dfs visit part for cycle detection
    """
    discovered.add(node)
    visiting.add(node)
    
    for neighbor in graph[node]: # 1
        if neighbor in visiting:
            return True
        if neighbor not in discovered:
            if dfs_has_cycle(graph, neighbor, discovered, visiting): # 
                return True

    visiting.remove(node)
    return False

def dfs_iterative(graph):
    """
    The outter loop for iterative version of dfs. It returns a list of nodes in topological order.
    """
    nodes_in_topo_order = deque([])
    discovered = set()
    nodes = [i for i in range(len(graph))]
    for node in nodes:
        if node not in discovered:
            dfs_visit_iterative(graph, node, discovered, nodes_in_topo_order)
    return list(nodes_in_topo_order)
        
def dfs_visit_iterative(graph, start, discovered, nodes_in_topo_order):
    """
    The iterative version of dfs visit. It returns a list of nodes that are reachable from start in topological order.
    """
    frontier = [(start, None)]
    parents = []
    discovered.add(start)
    
    while frontier or parents:
        if not frontier:
            while parents:
                nodes_in_topo_order.appendleft(parents.pop()[0])
            continue
        if not parents or frontier[-1][1] == parents[-1][0]:
            node, parent = frontier.pop()
            parents.append((node, parent))
            for neighbor in graph[node]:
                if neighbor not in discovered:
                    frontier.append((neighbor, node))
                    discovered.add(neighbor)
        else:
            nodes_in_topo_order.appendleft(parents.pop()[0])

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