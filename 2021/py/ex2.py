example = """
forward 5
down 5
forward 8
up 3
down 8
forward 2
"""


def parse_commands(data):
    lines = data.strip().split("\n")
    for l in lines:
        if not l.strip():
            continue
        litems = l.strip().split(" ")
        yield (litems[0], int(litems[1]))


def run_command(origin, cmd):
    (x, z) = origin
    (c, amount) = cmd
    if c == "forward":
        return (x + amount, z)
    elif c == "down":
        return (x, z + amount)
    elif c == "up":
        return (x, z - amount)


def run_commands(origin, commands, cmd=run_command):
    new_origin = origin
    for c in commands:
        new_origin = cmd(new_origin, c)
    return new_origin


def run_command2(origin, cmd):
    (x, z, aim) = origin
    (c, amount) = cmd
    if c == "forward":
        return (x + amount, z + amount * aim, aim)
    elif c == "down":
        return (x, z, aim + amount)
    elif c == "up":
        return (x, z, aim - amount)


def main():
    commands = parse_commands(open("ex2.txt").read())
    # commands = parse_commands(example)
    res = run_commands((0, 0, 0), commands, cmd=run_command2)
    print(res)
    print(res[0] * res[1])


if __name__ == "__main__":
    main()
