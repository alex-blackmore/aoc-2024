import re

with open("input.txt") as file:
    line = file.read().strip()
    mul = lambda x, y: x * y
    print(sum([eval(x) for x in re.findall(r'mul\(\d+,\d+\)', line)]))
    valid = line.split('don\'t()')[0] + ''.join([''.join(x.split('do()')[1:]) for x in line.split('don\'t()')[1:]])
    print(sum([eval(x) for x in re.findall(r'mul\(\d+,\d+\)', valid)]))
