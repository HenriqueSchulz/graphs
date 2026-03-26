from classes.node import Node

from pyvis.network import Network
from collections import deque
import webbrowser

class Graph:
    '''Implementation of a Graph'''

    def __init__(self):
        self.size = 0
        self.nodes: list[Node] = []
        self.edges = 0

    def add_node(self, node: Node):
        '''Add one node to graph list of nodes'''

        self.nodes.append(node)
        self.size += 1

    def remove_node(self, node: Node):
        '''Add one node to graph list of nodes'''

        if node in self.nodes:
            self.size -= 1
            self.edges -= node.degree
            self.nodes.remove(node)

    
    def add_edge(self, node1: Node, node2: Node, wheight: int):
        '''Add an edge between two nodes, if one of the two nodes not exists in the graph add this node'''

        node1.add_edge(node2, wheight)

        if node1 not in self.nodes:
            self.add_node(node1)

        if node2 not in self.nodes:
            self.add_node(node2)
        
        self.edges += 1

    def dijkstra(self, start_node: Node, end_node: Node):
        distances = {node: float('inf') for node in self.nodes}
        distances[start_node] = 0

        came_from = {}
        visited = set()

        while len(visited) < len(self.nodes):
            current = min(
                (n for n in self.nodes if n not in visited),
                key=lambda n: distances[n],
                default=None
            )

            if current is None:
                break

            if current == end_node:
                break

            visited.add(current)

            for neighbor, weight in current.nodes:
                new_dist = distances[current] + weight

                if new_dist < distances[neighbor]:
                    distances[neighbor] = new_dist
                    came_from[neighbor] = current

        path = []
        current = end_node

        while current in came_from:
            path.append(current)
            current = came_from[current]

        if current == start_node:
            path.append(start_node)
            path.reverse()
            return path, distances[end_node]

        return None, float('inf')

    def a_star(self, start_node: Node, end_node: Node):
        open_set = {start_node}
        came_from = {}

        g_score = {node: float('inf') for node in self.nodes}
        g_score[start_node] = 0

        f_score = {node: float('inf') for node in self.nodes}
        f_score[start_node] = getattr(start_node, "heuristic", 0)

        while open_set:
            current = min(open_set, key=lambda n: f_score[n])

            if current == end_node:
                path = []
                while current in came_from:
                    path.append(current)
                    current = came_from[current]
                path.append(start_node)
                path.reverse()
                return path, g_score[end_node]

            open_set.remove(current)

            for neighbor, weight in current.nodes:
                tentative_g = g_score[current] + weight

                if tentative_g < g_score[neighbor]:
                    came_from[neighbor] = current
                    g_score[neighbor] = tentative_g
                    f_score[neighbor] = (
                        tentative_g + getattr(neighbor, "heuristic", 0)
                    )
                    open_set.add(neighbor)

        return None, float('inf')

    def dfs(self, start_node: Node, target_node: Node):
        visited = set()
        came_from = {}

        def _dfs(current):
            if current == target_node:
                return True

            visited.add(current)

            for neighbor, _ in current.nodes:
                if neighbor not in visited:
                    came_from[neighbor] = current
                    if _dfs(neighbor):
                        return True

            return False

        found = _dfs(start_node)

        if not found:
            return None

        # Rebulding path
        path = []
        current = target_node

        while current in came_from:
            path.append(current)
            current = came_from[current]

        path.append(start_node)
        path.reverse()

        return path

    def bfs(self, start_node: Node, target_node: Node):
        visited = set([start_node])
        queue = deque([start_node])
        came_from = {}

        while queue:
            current = queue.popleft()

            if current == target_node:
                break

            for neighbor, _ in current.nodes:
                if neighbor not in visited:
                    visited.add(neighbor)
                    came_from[neighbor] = current
                    queue.append(neighbor)

        if target_node not in came_from and target_node != start_node:
            return None

        # Rebuilding path
        path = []
        current = target_node

        while current in came_from:
            path.append(current)
            current = came_from[current]

        path.append(start_node)
        path.reverse()

        return path

    def display(self):
        net = Network(directed=True)

        for node in self.nodes:
            net.add_node(id(node), label=str(node.value))

        for node in self.nodes:
            for neighbor, weight in node.nodes:
                net.add_edge(
                    id(node),
                    id(neighbor),
                    label=str(weight)
                )

        net.write_html("graph.html")
        webbrowser.open("graph.html")