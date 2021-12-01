"""
***** --- Day 21: Allergen Assessment --- *****
You reach the train's last stop and the closest you can get to your
vacation island without getting wet. There aren't even any boats here, but
nothing can stop you now: you build a raft. You just need a few days' worth
of food for your journey.
You don't speak the local language, so you can't read any ingredients
lists. However, sometimes, allergens are listed in a language you do
understand. You should be able to use this information to determine which
ingredient contains which allergen and work out which foods are safe to
take with you on your trip.
You start by compiling a list of foods (your puzzle input), one food per
line. Each line includes that food's ingredients list followed by some or
all of the allergens the food contains.
Each allergen is found in exactly one ingredient. Each ingredient contains
zero or one allergen. Allergens aren't always marked; when they're listed
(as in (contains nuts, shellfish) after an ingredients list), the
ingredient that contains each listed allergen will be somewhere in the
corresponding ingredients list. However, even if an allergen isn't listed,
the ingredient that contains that allergen could still be present: maybe
they forgot to label it, or maybe it was labeled in a language you don't
know.
For example, consider the following list of foods:
mxmxvkd kfcds sqjhc nhms (contains dairy, fish)
trh fvjkl sbzzf mxmxvkd (contains dairy)
sqjhc fvjkl (contains soy)
sqjhc mxmxvkd sbzzf (contains fish)
The first food in the list has four ingredients (written in a language you
don't understand): mxmxvkd, kfcds, sqjhc, and nhms. While the food might
contain other allergens, a few allergens the food definitely contains are
listed afterward: dairy and fish.
The first step is to determine which ingredients can't possibly contain any
of the allergens in any food in your list. In the above example, none of
the ingredients kfcds, nhms, sbzzf, or trh can contain an allergen.
Counting the number of times any of these ingredients appear in any
ingredients list produces 5: they all appear once each except sbzzf, which
appears twice.
Determine which ingredients cannot possibly contain any of the allergens in
your list. How many times do any of those ingredients appear?
To begin, get_your_puzzle_input.
Answer: [answer              ] [[Submit]]
You can also [Shareon Twitter Mastodon] this puzzle.
"""

from fastcore.all import L, Self
from util import *

e = Exercise(21, parser={"field_sep": "^$"})

@e.transformer(map=True)
def xform(row):
    r = row[0]
    ingr = set()
    algr = set()
    i, a = r.strip()[:-1].split(' (contains ')
    return set(i.split(' ')), set(a.split(', '))


import collections
import itertools

@e.part1()
def part1(xs):
    occurs = collections.Counter()
    mightbe = {}

    for (ingr, algr) in xs.t:
        for i in ingr:
            occurs[i] += 1

    for (ingr, algr) in xs.t:
        for a in algr:
            if a not in mightbe:
                mightbe[a] = set(ingr)
            else:
                mightbe[a] &= ingr

    return sum(occurs[k] for k in occurs if not any(k in m for m in mightbe.values()))

def setel(s):
    return next(iter(s))

def exclusive(xs):
    xs = list(xs)
    changed = True
    while changed:
        changed = False
        for x in xs:
            if len(x) != 1:
                continue
            r = setel(x)
            for y in xs:
                if r in y and len(y) > 1:
                    y.remove(r)
                    changed = True
    return xs

@e.part2()
def part2(xs):
    occurs = collections.Counter()
    occ_al = collections.Counter()
    mightbe = {}

    for (ingr, algr) in xs.t:
        for i in ingr:
            occurs[i] += 1
        for a in algr:
            occ_al[a] += 1

    for (ingr, algr) in xs.t:
        for a in algr:
            if a not in mightbe:
                mightbe[a] = set(ingr)
            else:
                mightbe[a] &= ingr


    exclusive(mightbe.values())
    return ','.join(setel(v) for _, v in sorted(mightbe.items()))





e()
