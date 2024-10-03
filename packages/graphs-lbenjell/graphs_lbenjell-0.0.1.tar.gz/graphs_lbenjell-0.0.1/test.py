from graphs_lbenjell import sp

def main():

    graph = {
        1: {2: 5, 3: 10},
        2: {1: 5, 3: 2, 4: 8},
        3: {1: 10, 2: 2, 4: 3},
        4: {2: 8, 3: 3}
    }
    
    # source node
    s = 1
    
    # This runs the Dijkstra's algorithm
    dist, path = sp.dijkstra(graph, s)
    
    # Print results
    print(f'Shortest distances from node {s}: {dist}')
    print(f'Shortest paths:')
    for node in path:
        print(f'Node {node}: {path[node]}')

if __name__ == '__main__':
    main()
