from pathlib import Path
import sys
import unittest
from math import inf

PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT))

from dijkstra import Graph, dijkstra, total_cost


class DijkstraTests(unittest.TestCase):
    def test_shortest_distances_are_calculated(self) -> None:
        graph = Graph(4)
        graph.add_edge(1, 2, 1)
        graph.add_edge(2, 3, 1)
        graph.add_edge(3, 4, 1)
        graph.add_edge(1, 4, 10)

        distances = dijkstra(graph, 1)

        self.assertEqual(distances[1:], [0, 1, 2, 3])
        self.assertEqual(total_cost(distances, 1), 6)

    def test_banned_edge_is_ignored(self) -> None:
        graph = Graph(3)
        graph.add_edge(1, 2, 1)
        graph.add_edge(2, 3, 1)
        banned_edge = graph.add_edge(1, 3, 1)

        distances = dijkstra(graph, 1, banned_edge=banned_edge)

        self.assertEqual(distances[3], 2)
        self.assertEqual(total_cost(distances, 1), 3)

    def test_unreachable_city_gives_infinite_cost(self) -> None:
        graph = Graph(3)
        graph.add_edge(1, 2, 5)

        distances = dijkstra(graph, 1)

        self.assertEqual(distances[3], inf)
        self.assertEqual(total_cost(distances, 1), inf)


if __name__ == "__main__":
    unittest.main()
