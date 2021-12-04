lines = open("ex3.txt").readlines()

n = len(lines[1]) - 1
print(lines[1])

data = lines


def part1():
    gamma = "0b"
    epsilon = "0b"
    print(data)
    for i in range(n):
        ones = 0
        zeros = 0
        for d in data:
            if d[i] == "1":
                ones += 1
            elif d[i] == "0":
                zeros += 1
        print(i, ones, zeros)
        if ones > zeros:
            gamma += "1"
            epsilon += "0"
        else:
            gamma += "0"
            epsilon += "1"

    g = eval(gamma)
    e = eval(epsilon)
    print(gamma, epsilon, g, e)
    print(g * e)


def keep_only_in_pos(pos, v, data):
    return [d for d in data if d[pos] == v]


def filter_out(dt, reversed=False):
    for i in range(n):
        ones = 0
        zeros = 0
        for d in dt:
            if d[i] == "1":
                ones += 1
            else:  # d[i] == "0"
                zeros += 1
        if not reversed:
            dt = keep_only_in_pos(i, "1" if ones >= zeros else "0", dt)
        else:
            dt = keep_only_in_pos(i, "0" if ones >= zeros else "1", dt)
        if len(dt) == 1:
            return dt[0]
        elif len(dt) == 0:
            raise ValueError("not found")


def part2():
    dt = list(data)
    oxy = filter_out(list(data))
    foo = filter_out(list(data), reversed=True)
    print(oxy, foo)
    oxy = int(oxy, 2)
    foo = int(foo, 2)
    print(oxy, foo)
    print(oxy * foo)


part2()
