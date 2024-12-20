import itertools as it

WALL = '#'
EMPTY = '.'
START = 'S'
END = 'E'
ALL_DIRECTIONS = [(-1, 0), (0, 1), (1, 0), (0, -1)]
REQUIRED_SAVE = 100
MAX_CHEAT_1 = 2
MAX_CHEAT_2 = 20

def adj(racetrack, i, j):
    return [(i + di, j + dj) for di, dj in ALL_DIRECTIONS if racetrack[i + di][j + dj] != WALL]

def dijkstra(racetrack):
    all_ij = list(it.product(range(len(racetrack)), range(len(racetrack[0]))))
    end = [(i, j) for (i, j) in all_ij if racetrack[i][j] == END][0]
    dist = {}
    prev = {}
    dist[end] = 0
    q = [(i, j) for i, j in all_ij if racetrack[i][j] != WALL]
    while q:
        mind = min([dist[v] for v in q if v in dist])
        u = [v for v in q if v in dist and dist[v] == mind][0]
        q.remove(u)
        nbs = adj(racetrack, *u)
        for nb in nbs:
            alt = dist[u] + 1
            if nb not in dist or dist[nb] > alt:
                dist[nb] = alt
                prev[nb] = u

    return dist

def edge(i, j, racetrack):
    return i == 0 or i == len(racetrack[0]) - 1 or j == 0 or j == len(racetrack) - 1

def reachable(i, j, dist, maxcheat):
    return [(ni, nj) for ni, nj in dist if abs(ni - i) + abs(nj - j) <= maxcheat]

def calculate_cheats(dist, maxcheat):
    cheats = []
    for cell in dist:
        for rcell in reachable(*cell, dist, maxcheat):
            i, j = cell
            ri, rj = rcell
            clength = abs(i - ri) + abs(j - rj)
            rlength = dist[(i, j)] - dist[(ri, rj)]
            if rlength - clength >= REQUIRED_SAVE:
                cheats.append(((i, j), rlength - clength))

    return len(cheats)

with open("input.txt") as file:
    racetrack = [[c for c in line] for line in file.read().strip().split("\n")]

    dist = dijkstra(racetrack)

    print(calculate_cheats(dist, MAX_CHEAT_1))
    print(calculate_cheats(dist, MAX_CHEAT_2))