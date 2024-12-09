import functools as ft
FREE = -1
UNUSED = -1

def real(i, c):
    if i % 2:
        return c * [FREE]
    else:
        return [(i // 2)] * c

def sof(rdisk):
    return ''.join([str(x[1]) * x[0] if x[1] != UNUSED else '.' * -x[0] for x in rdisk])

with open("input.txt") as file:
    disk = [int(c) for c in file.read().strip()]
    realdisk = ft.reduce(lambda x, y : x + y, [real(*x) for x in enumerate(disk)], [])

    for i, c in enumerate(realdisk[:]):
        # approx 50% required
        print(f"\r part 1: {round(i / len(realdisk) * 200, 2)}%", end="")
        if c == FREE:
            replaced = False
            for j in range(len(realdisk) - 1, i, -1):
                if realdisk[j] != FREE:
                    realdisk[i] = realdisk[j]
                    realdisk[j] = FREE
                    replaced = True
                    break
            if not replaced:
                break

    print()
    print(sum([i * x for i, x in enumerate(realdisk) if x != FREE]))

    realdisk = [[-x, UNUSED] if i % 2 else [x, i // 2] for i, x in enumerate(disk) if x]

    i = len(realdisk) - 1
    while True:
        print(f"\r part 2: {round((len(realdisk) - i - 1) / len(realdisk) * 100, 2)}%", end="")
        if i < 0: break
        space, index = realdisk[i]

        if space < 0:
            i -= 1
            continue
        
        for j in range(0, i):
            nspace, nindex = realdisk[j]
            if nspace > 0: continue
            if space + nspace > 0: continue
            realdisk[i] = [-space, UNUSED]
            realdisk[j] = [space, index]

            if space + nspace < 0:
                if (realdisk[j + 1][0] > 0):
                    realdisk = realdisk[:j + 1] + [[space + nspace, UNUSED]] + realdisk[j + 1:]
                    i += 1
                else:
                    ospace, oindex = realdisk[j + 1]
                    realdisk[j + 1] = [ospace + space + nspace, UNUSED]
            break

        i -= 1

    realrealdisk = ft.reduce(lambda x, y : x + y, [[x[1]] * x[0] if x[1] != UNUSED else [FREE] * -x[0] for x in realdisk])
    print()
    print(sum([i * x for i, x in enumerate(realrealdisk) if x != FREE]))