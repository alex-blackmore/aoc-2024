a = 105843716614554
b = 0
c = 0

result = []

while a != 0:
    b = a % 8
    c = a // (2 ** ((a % 8) ^ 5))
    b = (a % 8) ^ 3
    a = a // 8
    b ^= c
    print(b % 8, end=',')

print()