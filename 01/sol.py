with open("input.txt") as file:
    lines = [[int(x) for x in y.split()] for y in file.read().strip().split("\n")]
    s1, s2 = (sorted(l) for l in zip(*lines))
    print(sum(abs(x - y) for (x, y) in zip(s1, s2)))
    print(sum(s2.count(n) * n for n in s1))
    