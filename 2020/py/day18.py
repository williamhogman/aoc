"""
***** --- Day 18: Operation Order --- *****
As you look out the window and notice a heavily-forested continent slowly
appear over the horizon, you are interrupted by the child sitting next to
you. They're curious if you could help them with their math homework.
Unfortunately, it seems like this "math" follows_different_rules than you
remember.
The homework (your puzzle input) consists of a series of expressions that
consist of addition (+), multiplication (*), and parentheses ((...)). Just
like normal math, parentheses indicate that the expression inside must be
evaluated before it can be used by the surrounding expression. Addition
still finds the sum of the numbers on both sides of the operator, and
multiplication still finds the product.
However, the rules of operator precedence have changed. Rather than
evaluating multiplication before addition, the operators have the same
precedence, and are evaluated left-to-right regardless of the order in
which they appear.
For example, the steps to evaluate the expression 1 + 2 * 3 + 4 * 5 + 6 are
as follows:
1 + 2 * 3 + 4 * 5 + 6
  3   * 3 + 4 * 5 + 6
      9   + 4 * 5 + 6
         13   * 5 + 6
             65   + 6
                 71
Parentheses can override this order; for example, here is what happens if
parentheses are added to form 1 + (2 * 3) + (4 * (5 + 6)):
1 + (2 * 3) + (4 * (5 + 6))
1 +    6    + (4 * (5 + 6))
     7      + (4 * (5 + 6))
     7      + (4 *   11   )
     7      +     44
            51
Here are a few more examples:
    * 2 * 3 + (4 * 5) becomes 26.
    * 5 + (8 * 3 + 9 + 3 * 4 * 3) becomes 437.
    * 5 * 9 * (7 * 3 * 3 + 9 * 3 + (8 + 6 * 4)) becomes 12240.
    * ((2 + 4 * 9) * (6 + 9 * 8 + 6) + 6) + 2 + 4 * 2 becomes 13632.
Before you can help with the homework, you need to understand it yourself.
Evaluate the expression on each line of the homework; what is the sum of
the resulting values?
To begin, get_your_puzzle_input.
Answer: [answer              ] [[Submit]]
You can also [Shareon Twitter Mastodon] this puzzle.
"""

from fastcore.all import L, Self
from util import *

e = Exercise(18, parser = { "field_sep": r"(?:\s+)"})

@e.transformer(map=True)
def xform(toks):
    new_toks = []
    for tok in toks:
        if isinstance(tok, int) or len(tok) == 1:
            new_toks.append(tok)
        elif (tok[0]) == "(":
            n = sum(1 for c in tok if c == "(")
            for i in range(n):
                new_toks.append("(")
            new_toks.append(int(tok[n:]))
        elif tok[-1] == ")":
            n = sum(1 for c in tok if c == ")")
            new_toks.append(int(tok[:-n]))
            for i in range(n):
                new_toks.append(")")

    return new_toks


def pop_upto_left_paren(ops):
    while True:
        op = ops.pop()
        if op == '(':
            break
        yield op

def pop_before(ops, x, prec):
    while True:
        if not ops:
            return
        if ops[-1] not in ("+", "*"):
            return
        if not prec[ops[-1]] >= prec[x]:
            return

        yield ops.pop()

def syard(xs, prec):
    operators = []
    for x in xs:
        if x == '(':
            operators.append(x)
        elif x == ')':
            yield from pop_upto_left_paren(operators)
        elif isinstance(x, int):
            yield x
        else:
            yield from pop_before(operators, x, prec)
            operators.append(x)

    yield from reversed(operators)


def calc(xs):
    stack = []
    for token in xs:
        if token in ("*", "+",):
            arg2 = stack.pop()
            arg1 = stack.pop()
            if token == "*":
                result = arg1 * arg2
            elif token == "+":
                result = arg1 + arg2
            stack.append(result)
        else:
            stack.append(token)
    return stack.pop()


@e.part1(map=True, reduce="sum")
def part1(xs):
    return calc(syard(xs, { "+": 1, "*": 1 }))

@e.part2(map=True, reduce="sum")
def part2(xs):
    return calc(syard(xs, { "+": 2, "*": 1 }))







e()
