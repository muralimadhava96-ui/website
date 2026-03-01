# Dijkstra Implementation

Simple, dependency-free Python implementation of Dijkstra's shortest-path algorithm.

Usage:

Run the example:

```bash
python3 example.py
```

Run unit tests:

```bash
python3 -m unittest discover -v
```

Command-line interface:

You can run the CLI to compute shortest paths from a file-based graph. Examples below assume you're in the project directory.

- JSON adjacency list format (node -> list of [neighbor, weight]):

```bash
python3 dijkstra_cli.py --file graph.json --format json --source s --print-all
```

- Edge-list format (space-separated `u v [weight]` per line):

```bash
python3 dijkstra_cli.py --file graph.edgelist --format edgelist --source s --target t
```

The CLI prints distances or a specific path when `--target` is given. Use `--print-all` to list distances to all nodes.

API:

- `dijkstra(graph, source)`
  - `graph`: dict mapping node -> list of `(neighbor, weight)`
  - returns: `(distances, previous)` where `distances[node]` is shortest distance and
    `previous[node]` is the previous node on the shortest path (or `None`).

- `reconstruct_path(previous, target)` returns the path as a list of nodes from the
  source to `target` (empty if unreachable).

Notes:

- Graph should contain all nodes as keys (even if a node has an empty adjacency list).
- Weights must be non-negative.
