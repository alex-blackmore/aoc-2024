import itertools as it

def oob(g, x, y):
    return x < 0 or x >= len(g) or y < 0 or y >= len(g[0])

def xvalid(grid, x, y):
    for dir in filter(lambda x : x[0] or x[1], it.product([-1, 0, 1], [-1, 0, 1])):
        if any([oob(grid, x + n * dir[0], y + n * dir[1]) for n in range(4)]): continue
        if "".join([grid[x + n * dir[0]][y + n * dir[1]] for n in range(4)]) == "XMAS": yield dir

def avalid(grid, pos):
    allds = list(it.product([-1, 1], [-1, 1]))
    if any([oob(grid, pos[0] + dir[0], pos[1] + dir[1]) for dir in allds]): return False
    pat = [grid[pos[0] + dir[0]][pos[1] + dir[1]] for dir in allds]
    return not (pat.count('M') != 2 or pat.count('S') != 2 or pat[0] == pat[3])

with open("input.txt") as file:
    grid = [[c for c in line.strip()] for line in file.readlines()]
    allinds = list(it.product(range(len(grid)), range(len(grid[0]))))
    print(sum([len(list(xvalid(grid, x, y))) for (x, y) in allinds]))
    print(len([x for x in allinds if grid[x[0]][x[1]] == 'A' and avalid(grid, x)]))