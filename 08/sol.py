import itertools as it
from collections import defaultdict

freqs = defaultdict(list)
antinodes = []
eqs = []

def bounded(grid, i, j):
    return i >= 0 and i < len(grid) and j >= 0 and j < len(grid[0])

def anodes(x, y):
    xi, xj = x
    yi, yj = y
    di = yi - xi
    dj = yj - xj
    return [(xi - di, xj - dj), (yi + di, yj + dj)]


def process(freq):
    global antinodes, freqs
    nodes = freqs[freq]
    for (x, y) in it.combinations(nodes, 2):
        antinodes += anodes(x, y)

def eq_for(x, y):
    x1, y1 = x
    x2, y2 = y
    a = y1 - y2
    b = x2 - x1
    c = x2 * y1 - x1 * y2
    return lambda p : (a * p[0] + b * p[1] == c)

def process2(freq):
    global eqs, freqs
    nodes = freqs[freq]
    for (x, y) in it.combinations(nodes, 2):
        eqs.append(eq_for(x, y))

with open("input.txt") as file:
    grid = [[c for c in l] for l in file.read().strip().split("\n")]
    [freqs[grid[i][j]].append((i, j)) for i, j in it.product(range(len(grid)), range(len(grid[0]))) if grid[i][j] != '.']
    [process(freq) for freq in freqs.keys()]
    print(len(set([a for a in antinodes if bounded(grid, *a)])))
    [process2(freq) for freq in freqs.keys()]
    print(len([(i, j) for i, j in it.product(range(len(grid)), range(len(grid[0]))) if any([eq((i, j)) for eq in eqs])]))
