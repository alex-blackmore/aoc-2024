import re
import itertools as it

MAX_ITER = 100
A_COST = 3
B_COST = 1
REAL_OFFSET = 10000000000000

def bruteforce_best_cost(ax, ay, bx, by, tx, ty):
    best = None
    for na, nb in it.product(range(MAX_ITER + 1), repeat=2):
        if tx == (ax * na + bx * nb) and ty == (ay * na + by * nb):
            this_cost = na * A_COST + nb * B_COST
            if best == None or best > this_cost:
                best = this_cost
    if best == None: return 0
    return best

def calculate_best_cost(ax, ay, bx, by, tx, ty):
    tx += REAL_OFFSET
    ty += REAL_OFFSET
    # na, nb are unknown
    # eq1:
    #   ty = ay * na + by * nb
    # eq2:
    #  tx = ax * na + bx * nb
    # solve for na
    # bx * nb = tx - ax * na
    # multiply eq1 by bx
    # ty * bx = ay * bx * na + by * bx * nb
    # substitute bx * nb
    # ty * bx = ay * bx * na + by * (tx - ax * na)
    # expand
    # ty * bx = ay * bx * na + by * tx - by * ax * na
    # move na to one side
    # ty * bx - by * tx = ay * bx * na - by * ax * na
    # collect
    # ty * bx - by * tx = na (ay * bx - by * ax)
    # set for na
    # na = (ty * bx - by * tx) / (ay * bx - by * ax)
    na = (ty * bx - by * tx) // (ay * bx - by * ax)
    # solve for nb in eq1
    # ty = ay * na + by * nb
    # nb = (ty - ay * na) / by
    nb = (ty - ay * na) // by
    if tx != (ax * na + bx * nb) or ty != (ay * na + by * nb): return 0
    return na * A_COST + nb * B_COST


with open("input.txt") as file:
    games = [list(map(int, re.findall(r'\d+', g))) for g in file.read().strip().split("\n\n")]
    print(sum([bruteforce_best_cost(*g) for g in games]))
    print(sum([calculate_best_cost(*g) for g in games]))