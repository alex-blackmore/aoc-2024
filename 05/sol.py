def apply(arr, x, y):
    if x not in arr or y not in arr: return arr
    if (i := arr.index(x)) > (j := arr.index(y)):
        return arr[:j] + [arr[i]] + arr[j:i] + arr[i + 1:]
    return arr

def reorder(rules, arr):
    if good(rules, arr): return []
    while not good(rules, arr):
        for rule in rules:
            arr = apply(arr, *rule)
    return arr

def good(rules, arr):
    cr = lambda rule, arr : not (rule[0] in arr and rule[1] in arr and arr.index(rule[0]) > arr.index(rule[1]))
    return all([cr(rule, arr) for rule in rules])

with open("input.txt") as file:
    s1, s2 = file.read().split("\n\n")
    rules = [line.split("|") for line in s1.strip().split("\n")]
    updates = [arr.split(",") for arr in s2.strip().split("\n")]
    print(sum([int(arr[(len(arr) - 1) // 2]) for arr in updates if good(rules, arr)]))
    print(rules)
    # print(updates)
    mod = [reorder(rules, line) for line in updates if reorder(rules, line)]
    print(sum([int(arr[(len(arr) - 1) // 2]) for arr in mod]))