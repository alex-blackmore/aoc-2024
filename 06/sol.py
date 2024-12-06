from collections import defaultdict

visited = defaultdict(list)
gi = -1
gj = -1

CYCLE = 2
CONT = 1
DONE = 0

def rot(c):
    match (c):
        case '<': return '^'
        case '^': return '>'
        case '>': return 'v'
        case 'v': return '<'
    raise

def bounds(i, j, map):
    return i >= 0 and i < len(map) and j >= 0 and j < len(map[0])

def dir(g):
    match (g):
        case '<': return (0, -1)
        case '^': return (-1, 0)
        case '>': return (0, 1)
        case 'v': return (1, 0)
    raise

def guard(map):
    for i in range(len(map)):
        for j in range(len(map[0])):
            if map[i][j] in "<>^v":
                return (i, j)
    raise

def tick(map):
    global gi, gj
    i, j = gi, gj

    if map[i][j] in visited[(i, j)]:
        return CYCLE
    
    visited[(i, j)].append(map[i][j])
    di, dj = dir(map[i][j])

    if not bounds(i + di, j + dj, map):
        return DONE

    if (map[i + di][j + dj] == '#'):
        map[i][j] = rot(map[i][j])
    else:
        map[i + di][j + dj] = map[i][j]
        map[i][j] = "."
        gi += di
        gj += dj

    return CONT

with open("input.txt") as file:
    map = [[c for c in line] for line in file.read().strip().split("\n")]
    copy = [l[:] for l in map[:]]

    gi, gj = guard(map)
    while tick(map) == CONT: pass

    print(len(visited.keys()))

    total = 0
    iter = 0
    lp = dict.fromkeys(visited.keys(),[])
    for i, j in lp.keys():
        iter += 1
        visited = defaultdict(list)
        new_map = [l[:] for l in copy[:]]
        if new_map[i][j] in '<>^v': continue
        new_map[i][j] = '#'
        gi, gj = guard(new_map)
        while CONT == (res := tick(new_map)): pass
        if res == CYCLE:
            total += 1
        print('\r' + str(round(iter / len(lp.keys()) * 100, 2)) + '%', end="")
    
    print('\n' + repr(total))