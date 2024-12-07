import itertools as it

def solve(target, components):
    all = it.product(*([['+', '*']] * (len(components) - 1)))
    
    for ops in all:
        total = components[0]
        i = 0
        for c in components[1:]:
            if ops[i] == '+':
                total += c
            else:
                total *= c
            i += 1
        if total == target:
            return target

    return 0


# need to switch precedence (so enter "not cat" and bracket that)
def solve2(target, components):
    all = it.product(*([['+', '*', '||']] * (len(components) - 1)))
    
    for ops in all:
        total = components[0]
        i = 0
        for c in components[1:]:
            if ops[i] == '+':
                total += c
            elif ops[i] == '*':
                total *= c
            else:
                total = int(str(total) + str(c))
            i += 1
        if total == target:
            return target

    return 0

with open("input.txt") as file:
    rules = [(int(l.split(': ')[0]), [int(y) for y in l.split(': ')[1].split()]) for l in file.read().strip().split("\n")]  
    print(sum([solve(*r) for r in rules]))
    iter = 0
    total = 0
    for r in rules:
        total += solve2(*r)
        iter += 1
        print(f'\r{round(iter / len(rules) * 100, 2)}%', end="")
    print()
    print(sum([solve2(*r) for r in rules]))
