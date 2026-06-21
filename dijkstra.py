from __future__ import annotations

from dataclasses import dataclass, field
from heapq import heappop, heappush
from math import inf


@dataclass
class Graph_lite:
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

def dijkstra_lite(graph: Graph_lite, src: int) -> list[float, int]:
    distances = [[inf, 0] for _ in range(graph.n + 1)]
    visited = [False] * (graph.n + 1)
    distances[src][0] = 0
    distances[src][1] = -1
    visited[src] = True

    queue = []
    heappush(queue, (0, src))

    while(len(queue) != 0):
        current_cost, peak = heappop(queue)
        visited[peak] = True
        for target, weight in graph.adj[peak]:
            if current_cost + weight < distances[target][0]:
                distances[target][0] = current_cost + weight
                distances[target][1] = peak
            if(visited[target] == False):
                heappush(queue, (distances[target][0], target))

    return distances

def unused_connections(graph: Graph_lite, distances: list[list]):
    adj = [list(edges) for edges in graph.adj]
    for i in range(1,len(distances)):
        source = i
        target = distances[i][1]
        if(target == -1):
            continue
        for z in range(0,len(adj[i])):
            if(adj[i][z][0] == target):
                del adj[i][z]
                break

        for z in range(0,len(adj[target])):
            if(adj[target][z][0] == source):
                del adj[target][z]
                break

    return adj



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


def dijkstra_paths(
    graph: Graph, src: int, banned_edge: int | None = None
) -> tuple[list[float], list[int]]:
    distances = [inf] * (graph.n + 1)
    parents = [-1] * (graph.n + 1)
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
                parents[neighbor] = vertex
                heappush(queue, (candidate, neighbor))

    return distances, parents


def reconstruct_path(parents: list[int], src: int, dest: int) -> list[int]:
    if dest == src:
        return [src]
    path: list[int] = []
    v = dest
    while v != src and v != -1:
        path.append(v)
        v = parents[v]
    if v == -1:
        return []
    path.append(src)
    return path[::-1]
