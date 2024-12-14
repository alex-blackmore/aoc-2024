import re
import functools as ft

WIDTH = 101
HEIGHT = 103
PART_A_DURATION = 100
NORTHWEST = 0
NORTHEAST = 1
SOUTHEAST = 2
SOUTHWEST = 3
NO_QUADRANT = 4

def final_position(x, y, dx, dy, lx, ly, t):
    x += dx * t
    y += dy * t
    x %= lx
    y %= ly
    return (x, y)

def quadrant(x, y, lx, ly):
    hx = lx // 2
    hy = ly // 2
    if x < hx and y < hy:
        return NORTHWEST
    if x > hx and y < hy:
        return NORTHEAST
    if x > hx and y > hy:
        return SOUTHEAST
    if x < hx and y > hy:
        return SOUTHWEST
    return NO_QUADRANT

def print_grid(robots, t):
    final_pos = [final_position(*r, WIDTH, HEIGHT, t) for r in robots]
    for i in range(WIDTH):
        for j in range(HEIGHT):
            if (i, j) in final_pos:
                print('*', end="")
            else:
                print('.', end="")
        print()

with open("input.txt") as file:
    robots = [list(map(int, re.findall(r'-?\d+', line))) for line in file.read().strip().split("\n")]
    final_pos = [final_position(*r, WIDTH, HEIGHT, PART_A_DURATION) for r in robots]
    positions = [0, 0, 0, 0]
    for p in final_pos:
        q = quadrant(*p, WIDTH, HEIGHT)
        if q == NORTHEAST: positions[NORTHEAST] += 1
        if q == NORTHWEST: positions[NORTHWEST] += 1
        if q == SOUTHWEST: positions[SOUTHWEST] += 1
        if q == SOUTHEAST: positions[SOUTHEAST] += 1
    print(ft.reduce(lambda x, y : x * y, positions))

    # pattern first seen at 33 repeats every 101 (horizontal pattern)
    # pattern first seen at 87 repeats every 103 (vertical pattern)
    # need both at once
    #  33  134  235  336  437
    #  87  190  293  396  497
    # +54  +56  +58  +60  +62

    # need diff = 202 or 206 (202 happens first)

    # so need to run 101 - 27 = 74 cycles of 103 starting at 87
    # or equivalently 103 - 27 = 76 cycles of 101 starting at 33
    # need to run 87 + 74 * 103 == 33 + 76 * 101 times
    # which is equal to 7709

    print_grid(robots, 7709)
    print(f'the solution to part 2 is 7709')