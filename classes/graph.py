from classes.node import Node
from pyvis.network import Network
from collections import deque
import webbrowser
from math import radians, sin, cos, sqrt, atan2

class Graph:

    def __init__(self):
        self.size = 0
        self.nodes: list[Node] = []
        self.edges = 0

    def add_node(self, node: Node):
        self.nodes.append(node)
        self.size += 1

    def remove_node(self, node: Node):
        if node in self.nodes:
            self.size -= 1
            self.edges -= node.degree
            self.nodes.remove(node)

    def add_edge(self, node1: Node, node2: Node, wheight: int):
        node1.add_edge(node2, wheight)

        if node1 not in self.nodes:
            self.add_node(node1)

        if node2 not in self.nodes:
            self.add_node(node2)
        
        self.edges += 1

    def heuristic_zero(self, node: Node, goal: Node):
        return 0

    def heuristic_degree(self, node: Node, goal: Node):
        return abs(node.degree - goal.degree)

    def heuristic_geo(self, node: Node, goal: Node):
        if node.lat is None or goal.lat is None:
            return 0

        R = 6371000

        lat1, lon1 = radians(node.lat), radians(node.lon)
        lat2, lon2 = radians(goal.lat), radians(goal.lon)

        dlat = lat2 - lat1
        dlon = lon2 - lon1

        a = sin(dlat/2)**2 + cos(lat1)*cos(lat2)*sin(dlon/2)**2
        c = 2 * atan2(sqrt(a), sqrt(1-a))

        return R * c

    def dijkstra(self, start_node: Node, end_node: Node):
        distances = {node: float('inf') for node in self.nodes}
        distances[start_node] = 0

        came_from = {}
        visited = set()

        iterations = 0
        expanded_nodes = 0

        while len(visited) < len(self.nodes):
            iterations += 1

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
            expanded_nodes += 1

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

            return {
                "path": path,
                "cost": distances[end_node],
                "iterations": iterations,
                "expanded_nodes": expanded_nodes
            }

        return {
            "path": None,
            "cost": float('inf'),
            "iterations": iterations,
            "expanded_nodes": expanded_nodes
        }

    def a_star(self, start_node: Node, end_node: Node, heuristic_fn=None):
        
        if heuristic_fn is None:
            heuristic_fn = self.heuristic_geo
        
        open_set = {start_node}
        came_from = {}

        g_score = {node: float('inf') for node in self.nodes}
        g_score[start_node] = 0

        f_score = {node: float('inf') for node in self.nodes}
        f_score[start_node] = heuristic_fn(start_node, end_node)

        iterations = 0
        expanded_nodes = 0

        while open_set:
            iterations += 1

            current = min(open_set, key=lambda n: f_score[n])

            if current == end_node:
                path = []
                while current in came_from:
                    path.append(current)
                    current = came_from[current]
                path.append(start_node)
                path.reverse()

                return {
                    "path": path,
                    "cost": g_score[end_node],
                    "iterations": iterations,
                    "expanded_nodes": expanded_nodes
                }

            open_set.remove(current)
            expanded_nodes += 1

            for neighbor, weight in current.nodes:
                tentative_g = g_score[current] + weight

                if tentative_g < g_score[neighbor]:
                    came_from[neighbor] = current
                    g_score[neighbor] = tentative_g
                    f_score[neighbor] = (
                        tentative_g + heuristic_fn(neighbor, end_node)
                    )
                    open_set.add(neighbor)

        return {
            "path": None,
            "cost": float('inf'),
            "iterations": iterations,
            "expanded_nodes": expanded_nodes
        }

    def dfs(self, start_node: Node, target_node: Node):
        visited = set()
        came_from = {}

        iterations = 0
        expanded_nodes = 0

        def _dfs(current):
            nonlocal iterations, expanded_nodes

            iterations += 1

            if current == target_node:
                return True

            visited.add(current)
            expanded_nodes += 1

            for neighbor, _ in current.nodes:
                if neighbor not in visited:
                    came_from[neighbor] = current
                    if _dfs(neighbor):
                        return True

            return False

        found = _dfs(start_node)

        if not found:
            return {
                "path": None,
                "cost": None,
                "iterations": iterations,
                "expanded_nodes": expanded_nodes
            }

        path = []
        current = target_node

        while current in came_from:
            path.append(current)
            current = came_from[current]

        path.append(start_node)
        path.reverse()

        return {
            "path": path,
            "cost": None,
            "iterations": iterations,
            "expanded_nodes": expanded_nodes
        }

    def bfs(self, start_node: Node, target_node: Node):
        visited = set([start_node])
        queue = deque([start_node])
        came_from = {}

        iterations = 0
        expanded_nodes = 0

        while queue:
            iterations += 1

            current = queue.popleft()
            expanded_nodes += 1

            if current == target_node:
                break

            for neighbor, _ in current.nodes:
                if neighbor not in visited:
                    visited.add(neighbor)
                    came_from[neighbor] = current
                    queue.append(neighbor)

        if target_node not in came_from and target_node != start_node:
            return {
                "path": None,
                "cost": None,
                "iterations": iterations,
                "expanded_nodes": expanded_nodes
            }

        path = []
        current = target_node

        while current in came_from:
            path.append(current)
            current = came_from[current]

        path.append(start_node)
        path.reverse()

        return {
            "path": path,
            "cost": None,
            "iterations": iterations,
            "expanded_nodes": expanded_nodes
        }

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