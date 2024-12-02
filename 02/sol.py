def check(l):
    ds = [y - x for (x, y) in zip(l, l[1:])]
    if any(map(lambda x : abs(x) > 3, ds)): return False
    if abs(sum(map(lambda x : 0 if not x else x / abs(x), ds))) != len(ds): return False
    return True

def check_soft(l):
    return any([check(l[:i] + l[i + 1:]) for i in range(len(l))])

with open("input.txt") as file:
    lines = [[int(x) for x in l.split()] for l in file.read().strip().split("\n")]
    print(len(list(filter(check, lines))))
    print(len(list(filter(check_soft, lines))))
