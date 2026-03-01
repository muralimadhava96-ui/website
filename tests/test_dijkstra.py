import unittest
import sys
import os

# Ensure parent directory is on sys.path when running tests directly
here = os.path.dirname(os.path.abspath(__file__))
root = os.path.abspath(os.path.join(here, os.pardir))
if root not in sys.path:
    sys.path.insert(0, root)

from dijkstra import dijkstra, reconstruct_path


class TestDijkstra(unittest.TestCase):
    def test_basic_graph(self):
        graph = {
            'A': [('B', 1), ('C', 4)],
            'B': [('C', 2), ('D', 5)],
            'C': [('D', 1)],
            'D': []
        }
        dist, prev = dijkstra(graph, 'A')
        self.assertEqual(dist['A'], 0)
        self.assertEqual(dist['B'], 1)
        self.assertEqual(dist['C'], 3)
        self.assertEqual(dist['D'], 4)
        self.assertEqual(reconstruct_path(prev, 'D'), ['A', 'B', 'C', 'D'])

    def test_unreachable_node(self):
        graph = {'A': [('B', 1)], 'B': [], 'C': []}
        dist, prev = dijkstra(graph, 'A')
        self.assertEqual(dist['C'], float('inf'))
        self.assertEqual(prev['C'], None)

    def test_negative_weight_raises(self):
        graph = {'A': [('B', -1)], 'B': []}
        with self.assertRaises(ValueError):
            dijkstra(graph, 'A')


if __name__ == '__main__':
    unittest.main()
