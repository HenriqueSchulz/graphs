from classes import Graph
from classes import Node
from benchmark import Benchmark
from math import radians, sin, cos, sqrt, atan2

# =========================
# DISTÂNCIA REAL (Haversine)
# =========================
def real_distance(node1, node2):
    R = 6371000  # metros

    lat1, lon1 = radians(node1.lat), radians(node1.lon)
    lat2, lon2 = radians(node2.lat), radians(node2.lon)

    dlat = lat2 - lat1
    dlon = lon2 - lon1

    a = sin(dlat/2)**2 + cos(lat1)*cos(lat2)*sin(dlon/2)**2
    c = 2 * atan2(sqrt(a), sqrt(1-a))

    return round(R * c, 2)


graph = Graph()

# =========================
# NÓS COM COORDENADAS REAIS
# =========================
A = Node("CD", -25.45, -49.30)
B = Node("Centro", -25.4284, -49.2733)
C = Node("Batel", -25.4395, -49.2908)
D = Node("Agua Verde", -25.4522, -49.2804)
E = Node("Portao", -25.4765, -49.2943)
F = Node("CIC", -25.5070, -49.3345)
G = Node("Santa Felicidade", -25.3943, -49.3325)
H = Node("Boa Vista", -25.3820, -49.2467)
I = Node("Cabral", -25.4055, -49.2522)
J = Node("Alto da XV", -25.4180, -49.2605)
K = Node("Jardim Botanico", -25.4432, -49.2390)
L = Node("Uberaba", -25.4832, -49.2312)

nodes = [A,B,C,D,E,F,G,H,I,J,K,L]

for n in nodes:
    graph.add_node(n)

K_NEIGHBORS = 3

for node in nodes:
    distances = []

    for other in nodes:
        if node != other:
            dist = real_distance(node, other)
            distances.append((other, dist))

    distances.sort(key=lambda x: x[1])

    for neighbor, dist in distances[:K_NEIGHBORS]:
        graph.add_edge(node, neighbor, dist)

# =========================
# DEBUG
# =========================
#graph.display()
#print(f"Size: {graph.size}")
#print(f"Edges: {graph.edges}")

# =========================
# BENCHMARK
# =========================
benchmark = Benchmark(graph, rounds=5)

benchmark_results = benchmark.run(
    A,
    target_nodes=[E, F, G, H, I, J, K, L]
)

benchmark.display_table(benchmark_results)

benchmark_a_star_results = benchmark.run_a_star_test(
    A,
    target_nodes=[E, F, G, H, I, J, K, L]
)

benchmark.display_table(benchmark_a_star_results)