import heapq
from typing import Dict, List, Tuple, Any, Optional


def dijkstra(graph: Dict[Any, List[Tuple[Any, float]]], source: Any) -> Tuple[Dict[Any, float], Dict[Any, Optional[Any]]]:
    """Compute shortest paths from `source` to all reachable nodes using Dijkstra's algorithm.

    Args:
        graph: adjacency list mapping node -> list of (neighbor, weight).
        source: start node.

    Returns:
        distances: dict mapping node -> shortest distance from source (float('inf') if unreachable).
        previous: dict mapping node -> previous node on shortest path (None for source or unreachable).
    """
    distances: Dict[Any, float] = {node: float('inf') for node in graph}
    previous: Dict[Any, Optional[Any]] = {node: None for node in graph}

    if source not in graph:
        return distances, previous

    distances[source] = 0.0
    pq: List[Tuple[float, Any]] = [(0.0, source)]  # priority queue of (distance, node)

    while pq:
        dist_u, u = heapq.heappop(pq)
        if dist_u > distances[u]:
            continue

        for v, weight in graph.get(u, []):
            if weight < 0:
                raise ValueError("Dijkstra's algorithm does not support negative weights")
            alt = dist_u + weight
            if alt < distances.get(v, float('inf')):
                distances[v] = alt
                previous[v] = u
                heapq.heappush(pq, (alt, v))

    return distances, previous


def reconstruct_path(previous: Dict[Any, Optional[Any]], target: Any) -> List[Any]:
    """Reconstruct shortest path to `target` using `previous` map produced by `dijkstra`.

    Returns an empty list if target has no path (previous[target] is None and it's not the source).
    """
    path: List[Any] = []
    cur = target
    while cur is not None:
        path.append(cur)
        cur = previous.get(cur)
    path.reverse()
    return path


if __name__ == "__main__":
    sample_graph = {
        'A': [('B', 1), ('C', 4)],
        'B': [('C', 2), ('D', 5)],
        'C': [('D', 1)],
        'D': []
    }
    dist, prev = dijkstra(sample_graph, 'A')
    print('Distances:', dist)
    print('Path to D:', reconstruct_path(prev, 'D'))
