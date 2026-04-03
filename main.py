from classes import Graph
from classes import Node
from benchmark import Benchmark

graph = Graph()

# Neighborhoods
A = Node("CD")
B = Node("Centro")
C = Node("Batel")
D = Node("Agua Verde")
E = Node("Portao")
F = Node("CIC")
G = Node("Santa Felicidade")
H = Node("Boa Vista")
I = Node("Cabral")
J = Node("Alto da XV")
K = Node("Jardim Botanico")
L = Node("Uberaba")

nodes = [A,B,C,D,E,F,G,H,I,J,K,L]

for n in nodes:
    graph.add_node(n)

# =========================
# GRAFO ORIGINAL
# =========================
graph.add_edge(A, B, 5)
graph.add_edge(A, D, 7)
graph.add_edge(B, C, 4)
graph.add_edge(B, J, 6)
graph.add_edge(C, D, 3)
graph.add_edge(D, E, 5)
graph.add_edge(E, F, 8)
graph.add_edge(F, G, 10)
graph.add_edge(G, H, 6)
graph.add_edge(H, I, 4)
graph.add_edge(I, J, 3)
graph.add_edge(J, K, 5)
graph.add_edge(K, L, 7)
graph.add_edge(C, K, 6)
graph.add_edge(D, J, 4)
graph.add_edge(A, C, 9)
graph.add_edge(A, E, 10)
graph.add_edge(B, D, 6)
graph.add_edge(B, H, 11)
graph.add_edge(C, E, 4)
graph.add_edge(C, I, 7)
graph.add_edge(D, F, 6)
graph.add_edge(E, H, 5)
graph.add_edge(E, J, 9)
graph.add_edge(F, I, 3)
graph.add_edge(F, K, 8)
graph.add_edge(G, J, 4)
graph.add_edge(G, L, 2)
graph.add_edge(H, K, 6)
graph.add_edge(I, L, 5)

# Loops / Local cicles
graph.add_edge(D, B, 3)
graph.add_edge(E, C, 2)
graph.add_edge(F, D, 4)
graph.add_edge(H, E, 3)
graph.add_edge(I, F, 2)
graph.add_edge(J, G, 5)
graph.add_edge(K, H, 4)
graph.add_edge(L, I, 3)

# Loops / Larger cicles
graph.add_edge(A, G, 12)
graph.add_edge(G, D, 7)
graph.add_edge(B, I, 10)
graph.add_edge(I, C, 6)
graph.add_edge(E, L, 11)
graph.add_edge(L, A, 15)

#graph.display()
print(f"Size: {graph.size}")
print(f"Edges: {graph.edges}")

benchmark = Benchmark(graph, rounds=5)
#benchmark_results = benchmark.run(A, target_nodes=[E, F, G, H, I, J, K, L])
#benchmark.display_table(benchmark_results)
benchmark.run_a_star_test(A, target_nodes=[E, F, G, H, I, J, K, L], mode="on_the_fly")