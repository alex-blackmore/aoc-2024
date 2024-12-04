import itertools as it

def xvalid(grid, x, y):
    for dir in filter(lambda x : x[0] or x[1], it.product([-1, 0, 1], [-1, 0, 1])):
        if "".join([grid[x + n * dir[0]][y + n * dir[1]] for n in range(4)]) == "XMAS": yield dir

def avalid(grid, pos):
    pat = [grid[pos[0] + dir[0]][pos[1] + dir[1]] for dir in it.product([-1, 1], [-1, 1])]
    return not (pat.count('M') != 2 or pat.count('S') != 2 or pat[0] == pat[3])

with open("input.txt") as file:
    grid = ['.' * 1000] * 4 + ['....' + line.strip() + '....' for line in file.readlines()] + ['.' * 1000] * 4
    allinds = list(it.product(range(4, len(grid) - 4), range(4, len(grid[4]) - 4)))
    print(sum([len(list(xvalid(grid, x, y))) for (x, y) in allinds]))
    print(len([x for x in allinds if grid[x[0]][x[1]] == 'A' and avalid(grid, x)]))