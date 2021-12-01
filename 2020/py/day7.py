"""
***** --- Day 7: Handy Haversacks --- *****
You land at the regional airport in time for your next flight. In fact, it
looks like you'll even have time to grab some food: all flights are
currently delayed due to issues in luggage processing.
Due to recent aviation regulations, many rules (your puzzle input) are
being enforced about bags and their contents; bags must be color-coded and
must contain specific quantities of other color-coded bags. Apparently,
nobody responsible for these regulations considered how long they would
take to enforce!
For example, consider the following rules:
light red bags contain 1 bright white bag, 2 muted yellow bags.
dark orange bags contain 3 bright white bags, 4 muted yellow bags.
bright white bags contain 1 shiny gold bag.
muted yellow bags contain 2 shiny gold bags, 9 faded blue bags.
shiny gold bags contain 1 dark olive bag, 2 vibrant plum bags.
dark olive bags contain 3 faded blue bags, 4 dotted black bags.
vibrant plum bags contain 5 faded blue bags, 6 dotted black bags.
faded blue bags contain no other bags.
dotted black bags contain no other bags.
These rules specify the required contents for 9 bag types. In this example,
every faded blue bag is empty, every vibrant plum bag contains 11 bags (5
faded blue and 6 dotted black), and so on.
You have a shiny gold bag. If you wanted to carry it in at least one other
bag, how many different bag colors would be valid for the outermost bag?
(In other words: how many colors can, eventually, contain at least one
shiny gold bag?)
In the above rules, the following options would be available to you:
    * A bright white bag, which can hold your shiny gold bag directly.
    * A muted yellow bag, which can hold your shiny gold bag directly, plus
      some other bags.
    * A dark orange bag, which can hold bright white and muted yellow bags,
      either of which could then hold your shiny gold bag.
    * A light red bag, which can hold bright white and muted yellow bags,
      either of which could then hold your shiny gold bag.
So, in this example, the number of bag colors that can eventually contain
at least one shiny gold bag is 4.
How many bag colors can eventually contain at least one shiny gold bag?
(The list of rules is quite long; make sure you get all of it.)
To begin, get_your_puzzle_input.
Answer: [answer              ] [[Submit]]
You can also [Shareon Twitter Mastodon] this puzzle.
"""

from fastcore.all import L, Self
from util import *

e = Exercise(7, parser={'field_sep': r'bag[s]?(?:[\s\,\.])?(?:contain)?'})


def xform_item(item):
    item = item.strip()
    if "no other" in item:
        return None
    if item == "":
        return None
    l = item.split(" ")
    if len(l) == 2:
        return item
    elif len(l) == 3:
        return int(l[0]), l[1] + " " + l[2]

@e.transformer(map=True)
def xform(xs):
    l = L(xs).map(xform_item).filter(lambda x: x and x != "no other")
    return (l[0], l[1:])



def flip_d(d):
    flipped_d = {}
    for k in d:
        for b in d[k]:
            if b[1] not in flipped_d:
                flipped_d[b[1]] = set()
            flipped_d[b[1]].add(k)
    return flipped_d


@e.part1()
def part1(xs):
    d = dict(xs.t)

    flipped_d = flip_d(d)
    eventually_contains_gold = set(["shiny gold"])
    target = ["shiny gold"]
    while len(target):
        current = target.pop()
        eventually_contains_gold.add(current)
        for item in flipped_d.get(current, set()):
            target.append(item)

    return len(eventually_contains_gold) - 1

@e.part2()
def part2(xs):
    d = dict(xs.t)
    target = ["shiny gold"]
    so_far = 0
    while len(target):
        so_far += 1
        current = target.pop()
        for (cost, item) in d.get(current):
            target.extend([item] * cost)

    return so_far


e()
