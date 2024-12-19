import functools as ft
import sys

sys.setrecursionlimit(1000000)

@ft.cache
def num_ways(towel, patterns):
    if towel == '':
        return 0
    
    total = 0
    
    if towel in patterns:
        total += 1

    for p in patterns:
        if all(map(lambda x : x[0] == x[1], zip(towel, p))):
            total += num_ways(towel[len(p):], patterns)
    
    return total

with open("input.txt") as file:
    lines = file.read().strip().split("\n")
    patterns = tuple(lines[0].split(', '))
    towels = lines[1:]
    print(len([t for t in towels if num_ways(t, patterns)]))
    print(sum([num_ways(t, patterns) for t in towels]))