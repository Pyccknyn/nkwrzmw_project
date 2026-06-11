from __future__ import annotations

from dataclasses import dataclass, field
from heapq import heappop, heappush
from math import inf
import heapq


@dataclass
class Graph:
    n: int
    adj: list[list[tuple[int, float]]] = field(init=False)

    def __post_init__(self) -> None:
        self.adj = [[] for _ in range(self.n + 1)]

    def add_edge(self, u: int, v: int, weight: float) -> bool:
        if(u > self.n or v > self.n):
            return False
        if(u < 1 or v < 1):
            return False
        self.adj[u].append((v, weight))
        self.adj[v].append((u, weight))
        return True
    
    def print_edges(self):
        for i in range(1, len(self.adj)):
            print(f"source: {i}")
            for target, weight in self.adj[i]:
                print(f"     target: {target}   weight: {weight}")


def normal_dijkstra(graph: Graph, src: int) -> list[float, int]:
    distances = [[inf, 0] for _ in range(graph.n + 1)]
    visited = [False] * (graph.n + 1)
    distances[src][0] = 0
    distances[src][1] = -1
    visited[src] = True

    queue = []
    heapq.heappush(queue, (0, src))

    while(len(queue) != 0):
        current_cost, peak = heapq.heappop(queue)
        visited[peak] = True
        for target, weight in graph.adj[peak]:
            if current_cost + weight < distances[target][0]:
                distances[target][0] = current_cost + weight
                distances[target][1] = peak
            if(visited[target] == False):
                heapq.heappush(queue, (distances[target][0], target))

    return distances







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

