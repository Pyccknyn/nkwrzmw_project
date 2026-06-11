import dijkstra as dj

print("\n=== TEST 2: GRAF Z DIJKSTRA ===")
# Tworzymy graf o 7 wierzchołkach
graph = dj.Graph(n=7)

# Dodajemy krawędzie
graph.add_edge(1, 2, 2.0)
graph.add_edge(1, 3, 1.0)
graph.add_edge(1, 6, 8.0)  # Droga bezpośrednia, kusząca ale nieopłacalna

graph.add_edge(2, 3, 5.0)
graph.add_edge(2, 4, 2.0)
graph.add_edge(2, 5, 3.0)

graph.add_edge(3, 4, 1.5)

graph.add_edge(4, 6, 1.0)

graph.add_edge(5, 6, 1.0)
graph.add_edge(5, 7, 10.0) # Ślepy zaułek

graph.print_edges()

results = dj.normal_dijkstra(graph, 1)
for i in range(1, graph.n + 1):
    print(f"Wierzchołek {i} -> Koszt: {results[i][0]}, Poprzednik: {results[i][1]}")

