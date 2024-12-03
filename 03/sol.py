import re

with open("input.txt") as file:
    line = file.read().strip()
    mul = lambda x, y: x * y
    print(sum([eval(x) for x in re.findall(r'mul\(\d+,\d+\)', line)]))
    on = True
    total = 0
    instrs = re.findall(r"(mul\(\d+,\d+\))|(do\(\))|(don't\(\))", line)
    for inst in instrs:
        if inst[0] and on:
            total += eval(inst[0])
        elif not inst[0]:
            on = inst[1]
    print(total)
