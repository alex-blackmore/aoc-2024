import itertools as it

ALL_DIRS = [(0, 1), (0, -1), (1, 0), (-1, 0)]
PADDING = '.'
BOTTOM = 1
TOP = 2
RIGHT = 3
LEFT = 4
NO_EDGE = 0

def in_bounds(i, j, garden):
    return i >= 0 and i < len(garden) and j >= 0 and j < len(garden[0])

def adj(i, j):
    return [(i + di, j + dj) for di, dj in ALL_DIRS]

def expand_plot(plot, garden, t):
    done = False
    while not done:
        done = True
        for square in plot[:]:
            for a in adj(*square):
                if in_bounds(*a, garden) and garden[a[0]][a[1]] == t and a not in plot:
                    plot.append(a)
                    done = False
                

def cost(garden, visited, i, j):
    plot = [(i, j)]
    t = garden[i][j]
    expand_plot(plot, garden, t) 
    for p in plot:
        visited.append(p)
   
    area = len(plot)
    
    per = 0
    for p in plot:
        for a in adj(*p):
            if a not in plot:
                per += 1

    return area * per     

def count_sides(plot):
    mini = min(p[0] for p in plot)
    minj = min(p[1] for p in plot)
    maxi = max(p[0] for p in plot)
    maxj = max(p[1] for p in plot)

    edges = 0
    edge = NO_EDGE
    for i, j in it.product(range(mini - 1, maxi + 2), range(minj - 1, maxj + 2)):
        if (i, j) in plot and (i + 1, j) not in plot:
            if edge != BOTTOM:
                edge = BOTTOM
                edges += 1
        elif (i, j) not in plot and (i + 1, j) in plot:
            if edge != TOP:
                edge = TOP
                edges += 1
        else:
            edge = NO_EDGE
    
    edge = NO_EDGE
    for j, i in it.product(range(minj - 1, maxj + 2), range(mini - 1, maxi + 2)):
        if (i, j) in plot and (i, j + 1) not in plot:
            if edge != RIGHT:
                edge = RIGHT
                edges += 1
        elif (i, j) not in plot and (i, j + 1) in plot:
            if edge != LEFT:
                edge = LEFT
                edges += 1
        else:
            edge = NO_EDGE
    return edges

def bulk_cost(garden, visited, i, j):
    plot = [(i, j)]
    t = garden[i][j]
    expand_plot(plot, garden, t)
    for p in plot:
        visited.append(p)

    area = len(plot)
    sides = count_sides(plot)

    return area * sides

with open("input.txt") as file:
    garden = [[c for c in line] for line in file.read().strip().split()]
    price = 0
    visited = []
    for i, j in it.product(range(len(garden)), range(len(garden[0]))):
        if (i, j) in visited: continue
        price += cost(garden, visited, i, j)
    print(price)


    price = 0
    visited = []
    total_iters = len(garden) * len(garden[0])
    iter = 0
    for i, j in it.product(range(len(garden)), range(len(garden[0]))):
        iter += 1
        print(f'\r{round(iter / total_iters * 100, 2)}%', end='')
        if (i, j) in visited: continue
        price += bulk_cost(garden, visited, i, j)
    print()
    print(price)