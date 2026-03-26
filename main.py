from classes.graph import Graph
from classes.node import Node

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

#graph.display()
print(f"Size: {graph.size}")
print(f"Edges: {graph.edges}")