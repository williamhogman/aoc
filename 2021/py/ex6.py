ages = [int(x) for x in next(open("ex6.txt")).split(",")]
import collections

ages_short = [3, 4, 3, 1, 2]


def tick_for(fish):
    """
    After one day, its internal timer would become 2.
    After another day, its internal timer would become 1.
    After another day, its internal timer would become 0.
    After another day, its internal timer would reset to 6, and it would create a new lanternfish with an internal timer of 8.
    After another day, the first lanternfish would have an internal timer of 5, and the second lanternfish would have an internal timer of 7."""
    if fish == 0:
        return (6, 8)
    else:
        return (fish - 1, None)


def part1():
    fishes = ages
    for _ in range(80):
        add = []
        for i, fish in enumerate(fishes):
            (fish, new_fish) = tick_for(fish)
            if new_fish is not None:
                add.append(new_fish)
            fishes[i] = fish
        fishes.extend(add)


def part2():
    fishes = ages
    c = collections.Counter(fishes)
    for _ in range(256):
        new_c = collections.Counter()
        for k in c:
            (fish, new_fish) = tick_for(k)
            if new_fish is not None:
                new_c[new_fish] += c[k]
            new_c[fish] += c[k]
        c = new_c
    print(sum(c[k] for k in c))


def main():
    # part1()
    part2()


main()
