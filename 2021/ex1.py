# data = list(int(x.strip()) for x in open("ex1.txt").read() if x.strip())

data = []
for x in open("ex1.txt").readlines():
    data.append(int(x.strip()))


def ex1():
    increase = 0
    last_val = data[0]
    for i in data[1:]:
        if i > last_val:
            increase += 1
        last_val = i
        print(i, i > last_val)
    return increase


def wnd():
    for i in range(2, len(data)):
        if i >= 2:
            yield [data[i - 2], data[i - 1], data[i]]


def ex2():
    prev = -1
    cnt = 0
    for sliding_window in wnd():
        s = sum(sliding_window)
        print(sliding_window, s, prev, s > prev)
        if s > prev and prev != -1:
            cnt += 1
        prev = s
    return cnt


if __name__ == "__main__":
    # print(ex1())
    print(ex2())
