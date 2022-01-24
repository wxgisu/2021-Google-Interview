from typing import List, Set
from collections import deque

def dfs(graph):
    """
    This is the outter loop of the basic recursive version of DFS
    It returns the topological order of nodes as output. 
    This function is equivilent to topological sort
    """
    nodes_in_topo_order = deque([])
    return list(nodes_in_topo_order)

def dfs_visit(graph, node, discovered, nodes_in_topo_order):
    """
    This is the basic recursive version of DFS
    It uses a set to track discovered nodes, i.e. when nodes are FIRST seen
    It uses a double ended queue to populate nodes in topological order during DFS
    """
    pass
    
def strongly_connected_components(graph):
    """
    This returns the strongly connecte components of a graph in a list of list.
    """
    scc_list = []
    return scc_list

def build_reverse_graph(graph: List[List[int]]):
    reverse_graph = []
    return reverse_graph

def get_strongly_connected_components(graph, nodes):
    scc_list = []
    return scc_list

def dfs_visit_scc(graph, node, discovered, scc):
    pass
            
def has_cycle(graph):
    """
    Takes a graph as input, returns boolean representing is there is any cycle in the graph
    """
    pass

def dfs_has_cycle(graph, node, discovered, visiting): # 
    """
    This is the dfs visit part for cycle detection
    """
    pass

def dfs_iterative(graph):
    """
    The outter loop for iterative version of dfs. It returns a list of nodes in topological order.
    """
    nodes_in_topo_order = deque([])
    return list(nodes_in_topo_order)
        
def dfs_visit_iterative(graph, start, discovered, nodes_in_topo_order):
    """
    The iterative version of dfs visit. It returns a list of nodes that are reachable from start in topological order.
    """
    pass

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