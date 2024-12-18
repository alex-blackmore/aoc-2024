import itertools as it
import sys

sys.setrecursionlimit(1000000)

MEMORY_SIZE = 71    
NUM_BYTES = 1024
ALL_DIRECTIONS = [(-1, 0), (0, 1), (1, 0), (0, -1)]

def dijkstra(grid):
    dist = {}
    prev = {}
    dist[(0, 0)] = 0
    q = list(it.product(range(len(grid)), range(len(grid[0]))))

    while len(q) > 0:
        if all(v not in dist for v in q): break
        mdist = min(dist[v] for v in q if v in dist)
        u = [v for v in q if v in dist and dist[v] == mdist][0]
        q.remove(u)
        i, j = u
        nbs = [(i + di, j + dj) for (di, dj) in ALL_DIRECTIONS if (i + di, j + dj) in q]
        for v in nbs:
            if grid[v[0]][v[1]]: continue
            alt = dist[u] + 1
            if v not in dist or alt < dist[v]:
                dist[v] = alt
                prev[v] = u

    return dist, prev

def print_grid(grid):
    for i in range(len(grid)):
        for j in range(len(grid[0])):
            if grid[i][j]:
                print('#', end='')
            else:
                print('.', end='')
        print()

def bfs(grid, coord, visited):
    if coord in visited: return False
    visited.add(coord)
    if coord == (MEMORY_SIZE - 1, MEMORY_SIZE - 1): return True
    bounds = list(it.product(range(len(grid)), range(len(grid[0]))))
    i, j = coord
    nbs = [(i + di, j + dj) for (di, dj) in ALL_DIRECTIONS if (i + di, j + dj) in bounds and not grid[i + di][j + dj]]
    if len(nbs) == 0: return False
    return any(bfs(grid, nb, visited) for nb in nbs)

with open("input.txt") as file:
    bytes = [list(map(int, line.split(','))) for line in file.read().strip().split()]
    grid = [[False] * MEMORY_SIZE for _ in range(MEMORY_SIZE)]

    for byte in bytes[:NUM_BYTES]:
        grid[byte[1]][byte[0]] = True
    
    dist, prev = dijkstra(grid)
    print(dist[(MEMORY_SIZE - 1, MEMORY_SIZE - 1)])

    reachable = {}

    i = 0
    delt = len(bytes) // 2

    while True:
        if delt < 1: delt = 1
        grid = [[False] * MEMORY_SIZE for _ in range(MEMORY_SIZE)]
        for byte in bytes[:i]:
            grid[byte[1]][byte[0]] = True
        
        reachable[i] = bfs(grid, (0, 0), set())

        if not reachable[i] and i - 1 in reachable and reachable[i - 1]:
            print(','.join(map(str, bytes[i - 1])))
            break

        if reachable[i]:
            i += delt
            delt //= 2
        else:
            i -= delt
            delt //= 2