from __future__ import annotations

class Node:
    '''Implementation of a Node'''

    def __init__(self, value, lat=None, lon=None):
        '''Create a intance of a node'''

        self.value = value
        self.lat = lat
        self.lon = lon
        self.nodes: list[Node] = []      
        self.degree = 0
    
    def add_edge(self, node: Node, wheight):
        '''Add a edge between two nodes'''

        self.nodes.append((node, wheight))
        self.degree += 1
    
    def remove_edge(self, node: Node):
        '''Remove a edge between two nodes'''

        for i, (n, w) in enumerate(self.nodes):
            if n == node:
                del self.nodes[i]
                self.degree -= 1
                break
    
    def __hash__(self):
        return hash(id(self))