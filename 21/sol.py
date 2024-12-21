import functools as ft
import re

NUM_ROBOTS = 25

door_coords = {
    '7': (0, 0),
    '8': (0, 1),
    '9': (0, 2),
    '4': (1, 0),
    '5': (1, 1),
    '6': (1, 2),
    '1': (2, 0),
    '2': (2, 1),
    '3': (2, 2),
    '0': (3, 1),
    'A': (3, 2)
}

mv_translator = {
    ('A', 'A'): (('A', 'A'),),
    ('A', '^'): (('A', '<'), ('<', 'A')),
    ('A', '>'): (('A', 'v'), ('v', 'A')),
    ('A', 'v'): (('A', '<'), ('<', 'v'), ('v', 'A')),
    ('A', '<'): (('A', 'v'), ('v', '<'), ('<', '<'), ('<', 'A')),
    ('^', '^'): (('A', 'A'),),
    ('^', 'A'): (('A', '>'), ('>', 'A')),
    ('^', '>'): (('A', 'v'), ('v', '>'), ('>', 'A')),
    ('^', 'v'): (('A', 'v'), ('v', 'A')),
    ('^', '<'): (('A', 'v'), ('v', '<'), ('<', 'A')),
    ('>', '>'): (('A', 'A'),),
    ('>', '^'): (('A', '<'), ('<', '^'), ('^', 'A')),
    ('>', 'A'): (('A', '^'), ('^', 'A')),
    ('>', 'v'): (('A', '<'), ('<', 'A')),
    ('>', '<'): (('A', '<'), ('<', '<'), ('<', 'A')),
    ('v', 'v'): (('A', 'A'),),
    ('v', '^'): (('A', '^'), ('^', 'A')),
    ('v', '>'): (('A', '>'), ('>', 'A')),
    ('v', 'A'): (('A', '^'), ('^', '>'), ('>', 'A')),
    ('v', '<'): (('A', '<'), ('<', 'A')),
    ('<', '<'): (('A', 'A'),),
    ('<', '^'): (('A', '>'), ('>', '^'), ('^', 'A')),
    ('<', '>'): (('A', '>'), ('>', '>'), ('>', 'A')),
    ('<', 'v'): (('A', '>'), ('>', 'A')),
    ('<', 'A'): (('A', '>'), ('>', '>'), ('>', '^'), ('^', 'A'))
}

@ft.cache
def door_path(start, end):
    if start == end: return []
    # right/left then down
    # or up then left/right
    path = []
    si, sj = door_coords[start]
    ei, ej = door_coords[end]
    # down
    if ei >= si:
        # down before right
        if ej > sj:
            path += ['v'] * abs(ei - si)
            path += ['>'] * abs(ej - sj)
        # left before down
        else:
            path += ['<'] * abs(ej - sj)
            path += ['v'] * abs(ei - si)
    # up
    else:
        # put left first if possible
        if (ej != 0 or si != 3) and not ej > sj:
            path += ['<'] * abs(ej - sj)
            path += ['^'] * abs(ei - si)
        else:
        # up first
            path += ['^'] * abs(ei - si)
            if ej > sj:
                path += ['>'] * abs(ej - sj)
            else:
                path += ['<'] * abs(ej - sj)
    
    # print(f'{start} -> {end}: {''.join(path)}')
    return path

def door_input(code):
    inp = []
    fcode = ['A'] + code
    for s, e in zip(fcode, fcode[1:]):
        inp += door_path(s, e)
        inp.append('A')

    return inp

def fast_complexity(code, nrobots):
    num = int(re.findall(r'\d+', ''.join(code))[0])
    directions = ['A'] + door_input(code)
    movements = {}
    for s, e in zip(directions, directions[1:]):
        if (s, e) not in movements: movements[(s, e)] = [None, 0]
        movements[(s, e)][1] += 1

    for _ in range(nrobots):
        mk = [k for k in movements]
        for m in mk:
            movements[m][0] = 0

        for m in mk:
            for nm in mv_translator[m]:
                if nm not in movements: movements[nm] = [0, None]
                movements[nm][0] += movements[m][1]
        
        mk = [k for k in movements]
        for m in mk:
            movements[m][1] = movements[m][0]

    return sum([m[1] for m in movements.values()]) * num

with open("input.txt") as file:
    codes = [[c for c in line] for line in file.read().strip().split("\n")]
    print(sum(fast_complexity(c, 2) for c in codes))
    print(sum(fast_complexity(c, 25) for c in codes))
