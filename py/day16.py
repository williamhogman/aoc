"""
***** --- Day 16: Ticket Translation --- *****
As you're walking to yet another connecting flight, you realize that one of
the legs of your re-routed trip coming up is on a high-speed train.
However, the train ticket you were given is in a language you don't
understand. You should probably figure out what it says before you get to
the train station after the next flight.
Unfortunately, you can't actually read the words on the ticket. You can,
however, read the numbers, and so you figure out the fields these tickets
must have and the valid ranges for values in those fields.
You collect the rules for ticket fields, the numbers on your ticket, and
the numbers on other nearby tickets for the same train service (via the
airport security cameras) together into a single document you can reference
(your puzzle input).
The rules for ticket fields specify a list of fields that exist somewhere
on the ticket and the valid ranges of values for each field. For example, a
rule like class: 1-3 or 5-7 means that one of the fields in every ticket is
named class and can be any value in the ranges 1-3 or 5-7 (inclusive, such
that 3 and 5 are both valid in this field, but 4 is not).
Each ticket is represented by a single line of comma-separated values. The
values are the numbers on the ticket in the order they appear; every ticket
has the same format. For example, consider this ticket:
.--------------------------------------------------------.
| ????: 101    ?????: 102   ??????????: 103     ???: 104 |
|                                                        |
| ??: 301  ??: 302             ???????: 303      ??????? |
| ??: 401  ??: 402           ???? ????: 403    ????????? |
'--------------------------------------------------------'
Here, ? represents text in a language you don't understand. This ticket
might be represented as 101,102,103,104,301,302,303,401,402,403; of course,
the actual train tickets you're looking at are much more complicated. In
any case, you've extracted just the numbers in such a way that the first
number is always the same specific field, the second number is always a
different specific field, and so on - you just don't know what each
position actually means!
Start by determining which tickets are completely invalid; these are
tickets that contain values which aren't valid for any field. Ignore your
ticket for now.
For example, suppose you have the following notes:
class: 1-3 or 5-7
row: 6-11 or 33-44
seat: 13-40 or 45-50

your ticket:
7,1,14

nearby tickets:
7,3,47
40,4,50
55,2,20
38,6,12
It doesn't matter which position corresponds to which field; you can
identify invalid nearby tickets by considering only whether tickets contain
values that are not valid for any field. In this example, the values on the
first nearby ticket are all valid for at least one field. This is not true
of the other three nearby tickets: the values 4, 55, and 12 are are not
valid for any field. Adding together all of the invalid values produces
your ticket scanning error rate: 4 + 55 + 12 = 71.
Consider the validity of the nearby tickets you scanned. What is your
ticket scanning error rate?
To begin, get_your_puzzle_input.
Answer: [answer              ] [[Submit]]
You can also [Shareon Twitter Mastodon] this puzzle.
"""

from fastcore.all import L, Self
from util import *

e = Exercise(16)

def parse_rule(r):
    idx = list(r).index('or')
    low_range = (r[idx - 2], r[idx - 1])
    high_range = (r[idx + 1], r[idx + 2])
    name = " ".join(r[: idx - 2])
    return (name, low_range, high_range)


def ok_by_rule(rule, val):
    (_, (low_min, low_max), (high_min, high_max)) = rule
    return low_min <= val <= low_max or high_min <= val <= high_max

assert not ok_by_rule(("class", (1, 3), (5, 7)), 4)
assert not ok_by_rule(("class", (1, 3), (5, 7)), 0)
assert not ok_by_rule(("class", (1, 3), (5, 7)), 8)
assert ok_by_rule(("class", (1, 3), (5, 7)), 7)



@e.transformer()
def xform(xs):
    xs = xs.t
    i = 0
    rules = []
    while xs[i] != ("",):
        rules.append(parse_rule(xs[i]))
        i+= 1

    i += 2
    my_ticket = xs[i]
    i += 3

    nearby_tickets = xs[i:]
    return rules, my_ticket, nearby_tickets


def get_ticket_errors(rules, t):
    err = 0
    for f in t:
        if all(not ok_by_rule(r, f) for r in rules):
            err += f
    return err

R_TEST =     [
    ("class", (1, 3), (5, 7)),
    ("row", (6, 11), (33, 44)),
    ("seat", (13, 40), (45, 50)),
]
assert get_ticket_errors(
    R_TEST, [40,4,50]
) == 4

assert get_ticket_errors(
    R_TEST, [55,2,20]
) == 55

assert get_ticket_errors(
    R_TEST, [7,3,47]
) == 0

assert get_ticket_errors(
    R_TEST, [38,6,12]
) == 12


@e.part1()
def part1(xs):
    rules, my_ticket, nearby_tickets = xs

    err = 0
    for t in nearby_tickets:
        err += get_ticket_errors(rules, t)
    return err


def get_valid_rules(rules, v):
    for i, r in enumerate(rules):
        if ok_by_rule(r, v):
            yield i

@e.part2()
def part2(xs):
    rules, my_ticket, nearby_tickets = xs

    v_tick = [t for t in nearby_tickets if get_ticket_errors(rules, t) == 0]
    v_tick.append(my_ticket)


    n_fields = len(v_tick[0])
    n_rules = len(rules)
    cands = {i: set(range(n_rules)) for i in range(n_fields)}
    for t in v_tick:
        for i, f in enumerate(t):
            cands[i] = cands[i].intersection(set(get_valid_rules(rules, f)))

    while True:
        change = False
        for c in cands.values():
            if len(c) != 1:
                continue
            for c2 in cands.values():
                if c2 == c:
                    continue
                v = list(c)[0]
                if v in c2:
                    c2.remove(v)
                    change = True
        if not change:
            break

    fields = []
    for x in cands:
        cx = list(cands[x])
        if len(cx) == 1:
            c = cx[0]
            r = rules[c]
            print(x, r)
            if r[0].startswith("departure"):
                fields.append(x)
                assert len(cands[x]) == 1
        else:
            print(x, cx)



    res = 1
    for f in fields:
        res *= my_ticket[f]

    return res


e()
