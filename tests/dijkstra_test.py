from pathlib import Path
import sys
import unittest
from math import inf

PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT))

from dijkstra import Graph, dijkstra, total_cost, find_best_runway


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


    def test_find_best_runway_selects_optimal_edge(self) -> None:
        graph = Graph(4)
        id_expensive = graph.add_edge(1, 2, 10)  
        id_cheap = graph.add_edge(1, 2, 1)       
        graph.add_edge(2, 3, 1)
        graph.add_edge(2, 4, 1)
        
        best_edge_id, best_cost = find_best_runway(graph, 1)
        
        self.assertEqual(best_edge_id, id_expensive)
        self.assertEqual(best_cost, 5)

    def test_find_best_runway_returns_none_if_all_bridges(self) -> None:
        graph = Graph(3)
        graph.add_edge(1, 2, 5)
        graph.add_edge(2, 3, 5)
    
        best_edge_id, best_cost = find_best_runway(graph, 1)
        
        self.assertIsNone(best_edge_id)
        self.assertEqual(best_cost, inf)

if __name__ == "__main__":
    unittest.main()