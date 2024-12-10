import itertools as it

TRAILHEAD = 0
END = 10

def in_bounds(tmap, i, j):
    return i >= 0 and i < len(tmap) and j >= 0 and j < len(tmap[0])

def trails(tmap, i, j, looking_for, unique=False):
    if looking_for == END:
        return set([(i, j)]) if not unique else [(i, j)]
    
    found = set() if not unique else []
    for di, dj in it.product([0, 1, -1], repeat=2):
        if di and dj or not di and not dj: continue
        if not in_bounds(tmap, i + di, j + dj): continue
        if tmap[i + di][j + dj] != looking_for: continue
        if not unique:
            found = found.union(trails(tmap, i + di, j + dj, looking_for + 1, unique))
        else:
            found += trails(tmap, i + di, j + dj, looking_for + 1, unique)
    return found

with open("input.txt") as file:
    tmap = [[-1 if c == '.' else int(c) for c in line] for line in file.read().strip().split()]
    print(sum(len(trails(tmap, i, j, TRAILHEAD + 1)) for i, j in it.product(range(len(tmap)), range(len(tmap[0]))) if tmap[i][j] == TRAILHEAD))
    print(sum(len(trails(tmap, i, j, TRAILHEAD + 1, unique=True)) for i, j in it.product(range(len(tmap)), range(len(tmap[0]))) if tmap[i][j] == TRAILHEAD))