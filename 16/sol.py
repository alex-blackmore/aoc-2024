import itertools as it
import functools as ft

START = 'S'
END = 'E'
EMPTY = '.'
WALL = '#'
DIRECTIONS = [(-1, 0), (0, 1), (1, 0), (0, -1)]
NORTH, EAST, SOUTH, WEST = 0, 1, 2, 3

def dijkstra_shortest_path(maze, start, orientation, end):
    dist = {}
    dist[(start, orientation)] = 0
    prev = {}
    all_ij = it.product(range(len(maze)), range(len(maze[0])))
    vertices = list(it.product([(i, j) for i, j in all_ij if maze[i][j] != WALL], range(4)))
    iters = len(vertices)
    while len(vertices) > 0:
        
        print(f'\r{round((1 - ((len(vertices) - 1) / iters)) * 100, 2)}%', end='')

        # find vertex with smallest dist
        best_dist = min(dist[v] for v in vertices if v in dist)
        u = [v for v in vertices if v in dist and dist[v] == best_dist][0]
        vertices.remove(u)
        
        # find neighbours
        (i, j), dir = u
        di, dj = DIRECTIONS[dir]
        neighbours = [((i, j), (dir + 1) % 4), ((i, j), (dir - 1) % 4)]
        if maze[i + di][j + dj] != WALL: neighbours.append(((i + di, j + dj), dir))

        # calculate prev and dist
        for n in neighbours:
            nd = n[1]
            if nd != dir:
                alt = 1000 + dist[u]
            else:
                alt = 1 + dist[u]
            if n not in dist or dist[n] > alt:
                dist[n] = alt
                prev[n] = u
    print()

    return prev, dist

def best_cells(start, end, prev, dist):
    if end == start: return set([end[0]])

    # where could we have arrived at this cell from?
    known_dist = dist[end]
    (ei, ej), ed = end
    di, dj = DIRECTIONS[ed]

    # check if any other cells leading here have compatible dist
    possible_prev = [((ei, ej), (ed + 1) % 4), ((ei, ej), (ed - 1) % 4)]
    actual_prev = [p for p in possible_prev if known_dist == dist[p] + 1000]
    dpc = ((ei - di, ej - dj), ed)
    if dpc in dist and dist[dpc] + 1 == known_dist:
        actual_prev.append(((ei - di, ej - dj), ed))

    # recurse back to those cells
    result = set()
    for p in actual_prev:
        result = result.union(best_cells(start, p, prev, dist))
    result.add(end[0])

    return result

def print_maze(maze, best_cells, dist):
    # show best path
    for i in range(len(maze)):
        for j in range(len(maze[0])):
            if (i, j) in best_cells:
                print('O', end="")
            else:
                print(maze[i][j], end="")
        print()

    # show dijkstra values for all four directions for each cell (breaks for larger grids)
    for i in range(len(maze)):
        for j in range(len(maze[0])):
            if any(n in dist for n in it.product([(i, j)], range(4))):
                print(f'{dist[(i, j), NORTH] // 1000}{dist[(i, j), EAST] // 1000}', end="")
            else:
                print(maze[i][j] + maze[i][j], end="")
        print()
        for j in range(len(maze[0])):
            if any(n in dist for n in it.product([(i, j)], range(4))):
                print(f'{dist[(i, j), SOUTH] // 1000}{dist[(i, j), WEST] // 1000}', end="")
            else:
                print(maze[i][j] + maze[i][j], end="")
        print()

        
with open("input.txt") as file:
    maze = [[c for c in line] for line in file.read().strip().split("\n")]
    all_ij = list(it.product(range(len(maze)), range(len(maze[0]))))
    start = [(i, j) for i, j in all_ij if maze[i][j] == START][0]
    end = [(i, j) for i, j in all_ij if maze[i][j] == END][0]
    prev, dist = dijkstra_shortest_path(maze, start, EAST, end)
    best = min([dist[v] for v in it.product([end], range(4))])
    print(best)
    start = ((start), EAST)
    end = [e for e in it.product([end], range(4)) if dist[e] == best][0]
    print(len(best_cells(start, end, prev, dist)))

