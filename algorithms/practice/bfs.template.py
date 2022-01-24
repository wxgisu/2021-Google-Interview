from collections import deque
from typing import List

def bfs(graph):
    """
    This is the outter loop for the basic version of BFS.
    It tries to start from any un-discovered node in graph to perform BFS.
    This finds all connected components in a directed or undirected graph.
    """
    # Add implementation here
    pass
    
def bfs_visit(graph, start, discovered):
    """
    This is very basic version of BFS. 
    It uses a FIFO queue to implement the frontier.
    It uses a set to track nodes that are discovered. A node gets added to the discovered set the FIRST time its seen.
    """
    # Add implementation here
    pass

def bfs_visit_stand_alone(graph, start):
    """
    This is the stand alone implementation of the very basic version of BFS.
    The only difference between this method and bfs_visit is it doesn't take discovered as an argument.
    """
    # Add implementation here
    pass

def bfs_level_by_level(graph):
    """
    This is the outter loop for the level by level version of BFS.
    It also uses a set to track discovered nodes when nodes are first seen
    """
    # Add implementation here
    pass

def bfs_visit_level_by_level(graph, start, discovered):
    """
    This is the level by level version of BFS.
    It uses a list instead of FIFO queue to implement frontier.
    In a while loop
        it first copy full frontier list into result list, this maintains the FIFO order that nodes were added to frontier
        then it populates all nodes that can be discovered by nodes in frontier into a new list next_level_nodes
        then it updates frontier to next_level_nodes
    """
    # Add implementation here
    pass

def bfs_visit_level_by_level_stand_alone(graph, start):
    """
    This is the stand alone version of bfs_visit_level_by_level BFS.
    The only different between this method and bfs_visit_level_by_level is it doesn't take discovered set as input
    And it only starts from one node instead of all nodes. This only traverses nodes reachable from input node
    """
    # Add implementation here
    pass

def bfs_get_path(graph, start, target):
    """
    The variant of the base BFS that returns the shortest path from start to target.
    """
    # Add implementation here
    pass

def main():
    '''
        0 -> 1 -> 2 -> 4
                  ↓    ↑
                  3 ---+
    '''
    test1 = [
        [1], # 0
        [2], # 1
        [3, 4], # 2
        [4], # 3
        [],
    ]
    
    '''
        0 -> 1 -> 2 -> 4 -> 3
                  ↓    ↑
                  5 ---+
    '''
    test2 = [
        [1], # 0
        [2], # 1
        [4, 5], # 2
        [], # 3
        [3], # 4
        [], # 5
    ]

    t1, t1_res = bfs(test1), [[0, 1, 2, 3, 4]]
    t1_lbl, t1_lbl_res = bfs_level_by_level(test1), [[[0], [1], [2], [3, 4]]]
    t1_sa, t1_sa_res = bfs_visit_stand_alone(test1, 0), [0, 1, 2, 3, 4]
    t1_lbl_sa, t1_lbl_sa_res = bfs_visit_level_by_level_stand_alone(test1, 0), [[0], [1], [2], [3, 4]]
    t1_sp, t1_sp_res = bfs_get_path(test1, 0, 4), [0, 1, 2, 4]
    
    t2, t2_res = bfs(test2), [[0, 1, 2, 4, 5, 3]]
    t2_lbl, t2_lbl_res = bfs_level_by_level(test2), [[[0], [1], [2], [4, 5], [3]]]
    t2_sa, t2_sa_res = bfs_visit_stand_alone(test2, 0), [0, 1, 2, 4, 5, 3] 
    t2_lbl_sa, t2_lbl_sa_res = bfs_visit_level_by_level_stand_alone(test2, 0), [[0], [1], [2], [4, 5], [3]]
    t2_sp, t2_sp_res = bfs_get_path(test2, 0, 3), [0, 1, 2, 4, 3]
    
    tests = {
        't1': (t1, t1_res),
        't1_lbl': (t1_lbl, t1_lbl_res),
        't1_sa': (t1_sa, t1_sa_res),
        't1_lbl_sa': (t1_lbl_sa, t1_lbl_sa_res),
        't2': (t2, t2_res),
        't2_lbl': (t2_lbl, t2_lbl_res),
        't2_sa': (t2_sa, t2_sa_res),
        't2_lbl_sa': (t2_lbl_sa, t2_lbl_sa_res),
    }
    
    for test_name, test_data in tests.items():
        actual = test_data[0]
        expected = test_data[1]
        try:
            assert(actual == expected)
            print(f'{test_name} succeed')
        except:
            print(f'{test_name} failed')
    
if __name__ == '__main__':
    main()

