from __future__ import annotations

from dataclasses import dataclass, field
from heapq import heappop, heappush
from math import inf


@dataclass
class Graph:
    n: int
    adj: list[list[tuple[int, float, int]]] = field(init=False)
    edges: list[tuple[int, int, float]] = field(default_factory=list)

    def __post_init__(self) -> None:
        self.adj = [[] for _ in range(self.n + 1)]

    def add_edge(self, u: int, v: int, weight: float) -> int:
        edge_id = len(self.edges)
        self.edges.append((u, v, weight))
        self.adj[u].append((v, weight, edge_id))
        self.adj[v].append((u, weight, edge_id))
        return edge_id


def dijkstra(graph: Graph, src: int, banned_edge: int | None = None) -> list[float]:
    distances = [inf] * (graph.n + 1)
    distances[src] = 0

    queue: list[tuple[float, int]] = [(0, src)]

    while queue:
        current_distance, vertex = heappop(queue)

        if current_distance != distances[vertex]:
            continue

        for neighbor, weight, edge_id in graph.adj[vertex]:
            if edge_id == banned_edge:
                continue

            candidate = current_distance + weight
            if candidate < distances[neighbor]:
                distances[neighbor] = candidate
                heappush(queue, (candidate, neighbor))

    return distances


def total_cost(distances: list[float], src: int) -> float:
    total = 0

    for vertex, distance in enumerate(distances):
        if vertex == 0 or vertex == src:
            continue

        if distance == inf:
            return inf

        total += distance

    return total

def find_best_runway(graph: Graph, capital: int) -> tuple[int | None, float]:
  
    best_cost = inf
    best_edge_id = None
    
    for edge_id, (u, v, weight) in enumerate(graph.edges):
        distances = dijkstra(graph, capital, banned_edge=edge_id)
        current_cost = total_cost(distances, capital)
        
        if current_cost < best_cost:
            best_cost = current_cost
            best_edge_id = edge_id
            
    return best_edge_id, best_cost
