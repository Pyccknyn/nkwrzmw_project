import dijkstra as dj

g = dj.Graph_lite(4)
g.add_edge(1, 2, 1.0)
g.add_edge(2, 3, 2.0)
g.add_edge(1, 3, 5.0)  # Powinna być NIEUŻYWANA
g.add_edge(3, 4, 1.0)
g.add_edge(1, 4, 7.0)  # Powinna być NIEUŻYWANA

print("--- ORYGINALNY GRAF ---")
g.print_edges()

distances = dj.dijkstra_lite(g, src=1)

nieuzywane_listy = dj.unused_connections(g, distances)

print("\n--- POZOSTAŁE (NIEUŻYWANE) KRAWĘDZIE ---")
for i in range(1, len(nieuzywane_listy)):
    print(f"wierzchołek {i} ma nieużywane krawędzie do: {nieuzywane_listy[i]}")