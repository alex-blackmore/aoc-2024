import itertools as it

def solve(target, components, all_ops):
    all = it.product(*([all_ops] * (len(components) - 1)))
    
    for ops in all:
        total = components[0]
        for c, o in zip(components[1:], ops):
            match o:
                case '+': total += c
                case '*': total *= c
                case '||': total = int(str(total) + str(c))
                case _: raise
        if total == target:
            return target

    return 0

with open("input.txt") as file:
    rules = [(int(l.split(': ')[0]), [int(y) for y in l.split(': ')[1].split()]) for l in file.read().strip().split("\n")]  
    print(sum([solve(*r, ['+', '*']) for r in rules]))
    print(sum([solve(*r, ['+', '*', '||']) for r in rules]))
