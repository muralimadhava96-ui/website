#!/usr/bin/env python3
import argparse
import json
import sys
from typing import Dict, List, Tuple, Any

from dijkstra import dijkstra, reconstruct_path


def read_graph_json(path: str) -> Dict[Any, List[Tuple[Any, float]]]:
    with open(path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    # Expecting a dict node -> list of [neighbor, weight] or list of objects
    graph = {}
    for k, v in data.items():
        # Normalize into list of (neighbor, weight)
        edges = []
        for item in v:
            if isinstance(item, list) or isinstance(item, tuple):
                neighbor, weight = item[0], float(item[1])
            elif isinstance(item, dict):
                neighbor = item.get('to') or item.get('neighbor')
                weight = float(item.get('weight'))
            else:
                raise ValueError('Unrecognized edge format in JSON')
            edges.append((neighbor, weight))
        graph[k] = edges
    return graph


def read_edge_list(path: str) -> Dict[Any, List[Tuple[Any, float]]]:
    graph = {}
    with open(path, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith('#'):
                continue
            parts = line.split()
            if len(parts) < 2:
                continue
            u, v = parts[0], parts[1]
            w = float(parts[2]) if len(parts) >= 3 else 1.0
            graph.setdefault(u, []).append((v, w))
            # ensure v exists in graph keys
            graph.setdefault(v, graph.get(v, []))
    return graph


def main():
    p = argparse.ArgumentParser(description='Dijkstra CLI — compute shortest paths')
    p.add_argument('--file', '-f', help='Input graph file (JSON or edge list)')
    p.add_argument('--format', choices=['json', 'edgelist'], default='json', help='Input file format')
    p.add_argument('--source', '-s', required=True, help='Source node')
    p.add_argument('--target', '-t', help='Optional target node to show path for')
    p.add_argument('--print-all', action='store_true', help='Print distances for all nodes')

    args = p.parse_args()

    if not args.file:
        p.error('Please provide --file with graph input')

    if args.format == 'json':
        graph = read_graph_json(args.file)
    else:
        graph = read_edge_list(args.file)

    dist, prev = dijkstra(graph, args.source)

    if args.print_all:
        for node in sorted(graph.keys()):
            d = dist.get(node, float('inf'))
            print(f'{node}: {d}')
        return

    if args.target:
        if dist.get(args.target, float('inf')) == float('inf'):
            print(f'No path from {args.source} to {args.target}', file=sys.stderr)
            sys.exit(2)
        path = reconstruct_path(prev, args.target)
        print('distance:', dist[args.target])
        print('path: ' + ' -> '.join(path))
        return

    # default: print distances to all reachable nodes
    for node in sorted(dist.keys()):
        d = dist[node]
        if d == float('inf'):
            continue
        print(f'{node}: {d}')


if __name__ == '__main__':
    main()
