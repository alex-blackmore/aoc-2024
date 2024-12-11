import functools as ft

PASSES = 75
NEW = 0
OLD = 1

@ft.cache
def tick(stone):
    if not stone:
        return [1]
    if len(str(stone)) % 2 == 0:
        sstone = str(stone)
        return [int(sstone[:len(sstone) // 2]), int(sstone[len(sstone) // 2:])]
    else:
        return [2024 * stone]

with open("input.txt") as file:
    stones = {int(stone): [None, 1] for stone in file.read().strip().split()}

    for i in range(PASSES):
        okeys = [k for k in stones]
        for k in okeys:
            stones[k][NEW] = 0

        okeys = [k for k in stones]
        for k in okeys:
            new = tick(k)
            for n in new:
                if n not in stones: stones[n] = [0, None]
                stones[n][NEW] += stones[k][OLD]

        for k in stones:
            stones[k][OLD] = stones[k][NEW]

    print(sum(stones[k][0] for k in stones))