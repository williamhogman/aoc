"""
***** --- Day 19: Monster Messages --- *****
You land in an airport surrounded by dense forest. As you walk to your
high-speed train, the Elves at the Mythical Information Bureau contact you
again. They think their satellite has collected an image of a sea monster!
Unfortunately, the connection to the satellite is having problems, and many
of the messages sent back from the satellite have been corrupted.
They sent you a list of the rules valid messages should obey and a list of
received messages they've collected so far (your puzzle input).
The rules for valid messages (the top part of your puzzle input) are
numbered and build upon each other. For example:
0: 1 2
1: "a"
2: 1 3 | 3 1
3: "b"
Some rules, like 3: "b", simply match a single character (in this case, b).
The remaining rules list the sub-rules that must be followed; for example,
the rule 0: 1 2 means that to match rule 0, the text being checked must
match rule 1, and the text after the part that matched rule 1 must then
match rule 2.
Some of the rules have multiple lists of sub-rules separated by a pipe (|).
This means that at least one list of sub-rules must match. (The ones that
match might be different each time the rule is encountered.) For example,
the rule 2: 1 3 | 3 1 means that to match rule 2, the text being checked
must match rule 1 followed by rule 3 or it must match rule 3 followed by
rule 1.
Fortunately, there are no loops in the rules, so the list of possible
matches will be finite. Since rule 1 matches a and rule 3 matches b, rule 2
matches either ab or ba. Therefore, rule 0 matches aab or aba.
Here's a more interesting example:
0: 4 1 5
1: 2 3 | 3 2
2: 4 4 | 5 5
3: 4 5 | 5 4
4: "a"
5: "b"
Here, because rule 4 matches a and rule 5 matches b, rule 2 matches two
letters that are the same (aa or bb), and rule 3 matches two letters that
are different (ab or ba).
Since rule 1 matches rules 2 and 3 once each in either order, it must match
two pairs of letters, one pair with matching letters and one pair with
different letters. This leaves eight possibilities: aaab, aaba, bbab, bbba,
abaa, abbb, baaa, or babb.
Rule 0, therefore, matches a (rule 4), then any of the eight options from
rule 1, then b (rule 5): aaaabb, aaabab, abbabb, abbbab, aabaab, aabbbb,
abaaab, or ababbb.
The received messages (the bottom part of your puzzle input) need to be
checked against the rules so you can determine which are valid and which
are corrupted. Including the rules and the messages together, this might
look like:
0: 4 1 5
1: 2 3 | 3 2
2: 4 4 | 5 5
3: 4 5 | 5 4
4: "a"
5: "b"

ababbb
bababa
abbbab
aaabbb
aaaabbb
Your goal is to determine the number of messages that completely match rule
0. In the above example, ababbb and abbbab match, but bababa, aaabbb, and
aaaabbb do not, producing the answer 2. The whole message must match all of
rule 0; there can't be extra unmatched characters in the message. (For
example, aaaabbb might appear to match rule 0 above, but it has an extra
unmatched b on the end.)
How many messages completely match rule 0?
To begin, get_your_puzzle_input.
Answer: [answer              ] [[Submit]]
You can also [Shareon Twitter Mastodon] this puzzle.
"""

from fastcore.all import L, Self
from util import *

e = Exercise(19)


def groups(tok):
    grp = []
    for x in tok:
        if x == "|":
            yield grp
            grp = []
        else:
            grp.append(x)
    yield grp

def parse_tok(tok):
    if len(tok) == 1:
        if isinstance(tok[0], str) and tok[0][0] == '"':
            return ("LIT", tok[0].strip('"'))
        else:
            return ("RULES", [tok[0]])
    else:
        sub_rules = []
        for g in groups(tok):
            sub_rules.append(("RULES", g))
        if len(sub_rules) > 1:
            return ("OR", sub_rules)
        else:
            return sub_rules[0]




@e.transformer()
def xform(xs):
    d = {}
    msgs = []
    part2 = False
    for x in xs.t:
        if len(x) == 1 and x[0] == "":
            part2 = True
            continue
        if not part2:
            d[x[0]] = parse_tok(x[1:])
        else:
            assert len(x) == 1
            msgs.append(x[0])
    return d, msgs

EXAMPLE_RULES = """
0: 4 1 5
1: 2 3 | 3 2
2: 4 4 | 5 5
3: 4 5 | 5 4
4: "a"
5: "b"
"""




def eval_rule(rule, rules, message):
    op, arg = rule
    if op == "RULES":
        alt_suffixes = [message]
        for part in arg:
            alt_suffixes = [new_suffix for suffix in alt_suffixes for new_suffix in eval_rule(rules[part], rules, suffix)]
            if not alt_suffixes:
                break
        return alt_suffixes

        return [cur]
    elif op == "OR":
        suffixes = []
        for alt in arg:
            alt_suffixes = [message]
            for part in alt[1]:
                alt_suffixes = [new_suffix for suffix in alt_suffixes for new_suffix in eval_rule(rules[part], rules, suffix)]
                if not alt_suffixes:
                    break
            suffixes += alt_suffixes
        return suffixes
    elif op == "LIT":
        if not message:
            return []
        if arg == message[0]:
            return [message[1:]]
        else:
            return []
    assert False

def eval_rules(rules, message):
    r = rules[0]
    return eval_rule(r, rules, message)


@e.part1()
def part1(xs):
    (rules, msgs) = xs

    matching = 0
    for m in msgs:
        e = eval_rules(rules, m)
        if e == "":
            matching += 1

    return matching


def simplify_rule(rule, rules):
    op, arg = rule
    if op == "LIT":
        return rule
    elif op == "OR":
        new_sr = []
        for sr in arg:
            simp = simplify_rule(sr, rules)
            if simp[0] == "OR":
                for x in simp[1]:
                    new_sr.append(x)
            elif simp not in new_sr:
                new_sr.append(simp)
        return ("OR", new_sr)
    elif op == "RULES":
        if len(arg) == 1:
            return rules[arg[0]]
        else:
            return rule
    assert False

def simplify_rules(rules):
    for i in range(100):
        for k in rules:
            simp = simplify_rule(rules[k], rules)
            if simp != rules[k]:
                print("SIMP", k, rules[k], "-->", simp)
                rules[k] = simp
    return rules



@e.part2()
def part2(xs):
    (rules, msgs) = xs
    rules[8] = ("OR", [("RULES", [42]), ("RULES", [42, 8])])
    rules[11] = ("OR", [("RULES", [42, 31]), ("RULES", [42, 11, 31])])

    #rules = simplify_rules(rules)

    matching = 0
    for m in msgs:
        e = eval_rules(rules, m)
        if '' in e:
            matching += 1

    return matching

e()
