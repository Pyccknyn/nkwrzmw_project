from __future__ import annotations

import re

from dijkstra import Graph


def load_graph(filename: str) -> Graph:
    edges: list[tuple[int, int, float]] = []
    max_vertex = 0

    with open(filename, "r", encoding="utf-8") as f:
        pattern = r"(\d+),(\d+),(\d+(?:\.\d+)?)"
        for line in f:
            m = re.search(pattern, line)
            if m:
                u, v = int(m.group(1)), int(m.group(2))
                w = float(m.group(3))
                edges.append((u, v, w))
                max_vertex = max(max_vertex, u, v)

    if not edges:
        raise ValueError(f"Brak danych w pliku '{filename}'")

    graph = Graph(max_vertex)
    for u, v, w in edges:
        graph.add_edge(u, v, w)

    return graph
