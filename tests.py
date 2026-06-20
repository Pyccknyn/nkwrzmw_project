import dijkstra as dj
import re

g1 = dj.Graph_lite(20)  # Zmieniłem na 7, aby pomieścić wierzchołki od 1 do 6
g2 = dj.Graph(20)

with open("dane.txt", "r", encoding="utf-8") as file:
    pattern = r"(\d+),(\d+),(\d+)"
    for line in file:
        match = re.search(pattern, line)
        if match:
            source, target, weight = match.groups()
            g1.add_edge(int(source), int(target), int(weight))  # <- TUTAJ: Dodatkowe wcięcie!
            g2.add_edge(int(source), int(target), float(weight))


print("--- ORYGINALNY GRAF ---")
g1.print_edges()

distances = dj.dijkstra_lite(g1, src=1)

nieuzywane_listy = dj.unused_connections(g1, distances)

print("\n--- POZOSTAŁE (NIEUŻYWANE) KRAWĘDZIE ---")
for i in range(1, len(nieuzywane_listy)):
    print(f"wierzchołek {i} ma nieużywane krawędzie do: {nieuzywane_listy[i]}")