from collections import deque
from typing import Set


class Node:
    def __init__(self, label: str):
        self.label = label

class Graph:
    def __init__(self):
        self.nodes = {}
        self.adjacency_list = {}
        # TODO: lookup python dictionary putIfAbsent equevilent
        # TODO: check python avoid typing self.var in methods
        
    def add_node(self, label: str):
        node = Node(label)
        self.nodes.setdefault(label, node)
        self.adjacency_list.setdefault(node, [])
    
    def remove_node(self, label: str):
        if label not in self.nodes:
            return

        node = self.nodes[label]
        for to_nodes in self.adjacency_list.values():
            try:
                to_nodes.remove(node)
            except:
                pass
        self.nodes.pop(label)
        self.adjacency_list.pop(node)
            
    def add_edge(self, from_label: str, to_label: str):
        if (from_label not in self.nodes or
            to_label not in self.nodes):
            raise ValueError
        
        from_node = self.nodes[from_label]
        to_node = self.nodes[to_label]
        
        self.adjacency_list[from_node].append(to_node)
        
    def print(self):
        for node_label,node in self.nodes.items():
            for neighbor in self.adjacency_list[node]:
                print(f'{node_label} --> {neighbor.label}')
    
    def remove_edge(self, from_label: str, to_label: str):
        if (from_label not in self.nodes or
            to_label not in self.nodes):
            return
        
        from_node = self.nodes[from_label]
        to_node = self.nodes[to_label]
        try:
            self.adjacency_list[from_node].remove(to_node)
        except ValueError:
            print(f'{from_label} does not have an edge to {to_label}')
    
    def dfs(self, root: str):
        if root not in self.nodes:
            return
        # self.dfs_explore(root, set())
        self.dfs_explore_iterative(root, set())
    
    def dfs_explore(self, root: str, visited: Set):
        print(root)
        root_node = self.nodes[root]
        visited.add(root_node)

        for neighbor in self.adjacency_list[root_node]:
            if neighbor not in visited:
                self.dfs_explore(neighbor.label, visited)
    
    def dfs_explore_iterative(self, root: str, visited: Set):
        stack = []
        root_node = self.nodes[root]
        stack.append(root_node)
        
        while stack:
            current_node = stack.pop()
            print(current_node.label)
            visited.add(current_node)

            for neighbor in self.adjacency_list[current_node]:
                if neighbor not in visited:
                    stack.append(neighbor)
                    
    def bfs(self, root: str):
        if root not in self.nodes:
            return
        self.bfs_explore(root, set())

    def bfs_explore(self, root: str, visited: Set):
        queue = deque([])
        root_node = self.nodes[root]
        queue.append(root_node)
        
        while queue:
            current_node = queue.popleft()
            if current_node in visited:
                continue
            print(current_node.label)
            visited.add(current_node)
            for neighbor in self.adjacency_list[current_node]:
                if neighbor not in visited:
                    queue.append(neighbor)

def main():
    graph = Graph()
    graph.add_node('0')
    graph.add_node('1')
    graph.add_node('2')
    graph.add_node('3')
    graph.add_edge('0', '1')
    graph.add_edge('0', '2')
    graph.add_edge('2', '3')
    graph.print()
    print()
    graph.bfs('0')

if __name__ == '__main__':
    main()
