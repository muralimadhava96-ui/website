from dijkstra import dijkstra, reconstruct_path


def main():
    graph = {
        's': [('a', 7), ('b', 2), ('c', 3)],
        'a': [('s', 7), ('b', 3), ('d', 4)],
        'b': [('s', 2), ('a', 3), ('d', 4), ('e', 1)],
        'c': [('s', 3), ('e', 5)],
        'd': [('a', 4), ('b', 4), ('e', 1)],
        'e': [('b', 1), ('c', 5), ('d', 1)],
    }

    dist, prev = dijkstra(graph, 's')

    print('Shortest distances from s:')
    for node in sorted(dist.keys()):
        print(f'  {node}: {dist[node]}')

    print('\nExample paths:')
    for target in ['a', 'b', 'c', 'd', 'e']:
        path = reconstruct_path(prev, target)
        print(f'  s -> {target}:', ' -> '.join(path))


if __name__ == '__main__':
    main()
