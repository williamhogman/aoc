"""
***** --- Day 22: Crab Combat --- *****
It only takes a few hours of sailing the ocean on a raft for boredom to
sink in. Fortunately, you brought a small deck of space_cards! You'd like
to play a game of Combat, and there's even an opponent available: a small
crab that climbed aboard your raft before you left.
Fortunately, it doesn't take long to teach the crab the rules.
Before the game starts, split the cards so each player has their own deck
(your puzzle input). Then, the game consists of a series of rounds: both
players draw their top card, and the player with the higher-valued card
wins the round. The winner keeps both cards, placing them on the bottom of
their own deck so that the winner's card is above the other card. If this
causes a player to have all of the cards, they win, and the game ends.
For example, consider the following starting decks:
Player 1:
9
2
6
3
1

Player 2:
5
8
4
7
10
This arrangement means that player 1's deck contains 5 cards, with 9 on top
and 1 on the bottom; player 2's deck also contains 5 cards, with 5 on top
and 10 on the bottom.
The first round begins with both players drawing the top card of their
decks: 9 and 5. Player 1 has the higher card, so both cards move to the
bottom of player 1's deck such that 9 is above 5. In total, it takes 29
rounds before a player has all of the cards:
-- Round 1 --
Player 1's deck: 9, 2, 6, 3, 1
Player 2's deck: 5, 8, 4, 7, 10
Player 1 plays: 9
Player 2 plays: 5
Player 1 wins the round!

-- Round 2 --
Player 1's deck: 2, 6, 3, 1, 9, 5
Player 2's deck: 8, 4, 7, 10
Player 1 plays: 2
Player 2 plays: 8
Player 2 wins the round!

-- Round 3 --
Player 1's deck: 6, 3, 1, 9, 5
Player 2's deck: 4, 7, 10, 8, 2
Player 1 plays: 6
Player 2 plays: 4
Player 1 wins the round!

-- Round 4 --
Player 1's deck: 3, 1, 9, 5, 6, 4
Player 2's deck: 7, 10, 8, 2
Player 1 plays: 3
Player 2 plays: 7
Player 2 wins the round!

-- Round 5 --
Player 1's deck: 1, 9, 5, 6, 4
Player 2's deck: 10, 8, 2, 7, 3
Player 1 plays: 1
Player 2 plays: 10
Player 2 wins the round!

...several more rounds pass...

-- Round 27 --
Player 1's deck: 5, 4, 1
Player 2's deck: 8, 9, 7, 3, 2, 10, 6
Player 1 plays: 5
Player 2 plays: 8
Player 2 wins the round!

-- Round 28 --
Player 1's deck: 4, 1
Player 2's deck: 9, 7, 3, 2, 10, 6, 8, 5
Player 1 plays: 4
Player 2 plays: 9
Player 2 wins the round!

-- Round 29 --
Player 1's deck: 1
Player 2's deck: 7, 3, 2, 10, 6, 8, 5, 9, 4
Player 1 plays: 1
Player 2 plays: 7
Player 2 wins the round!


== Post-game results ==
Player 1's deck:
Player 2's deck: 3, 2, 10, 6, 8, 5, 9, 4, 7, 1
Once the game ends, you can calculate the winning player's score. The
bottom card in their deck is worth the value of the card multiplied by 1,
the second-from-the-bottom card is worth the value of the card multiplied
by 2, and so on. With 10 cards, the top card is worth the value on the card
multiplied by 10. In this example, the winning player's score is:
   3 * 10
+  2 *  9
+ 10 *  8
+  6 *  7
+  8 *  6
+  5 *  5
+  9 *  4
+  4 *  3
+  7 *  2
+  1 *  1
= 306
So, once the game ends, the winning player's score is 306.
Play the small crab in a game of Combat using the two decks you just dealt.
What is the winning player's score?
To begin, get_your_puzzle_input.
Answer: [answer              ] [[Submit]]
You can also [Shareon Twitter Mastodon] this puzzle.
"""

from fastcore.all import L, Self
from util import *

e = Exercise(22)

@e.transformer()
def xform(xs):

    return (
        [40,
         28,
         39,
         7,
         6,
         16,
         1,
         27,
         38,
         8,
         15,
         3,
         26,
         9,
         30,
         5,
         50,
         17,
         20,
         45,
         34,
         10,
         21,
         14,
         43],
        [
            4,
            49,
            35,
            11,
            32,
            12,
            48,
            23,
            47,
            22,
            46,
            13,
            18,
            41,
            24,
            36,
            37,
            44,
            19,
            42,
            33,
            25,
            2,
            29,
            31
        ]
    )


    player = 1
    decks = ([], [])
    for row in xs.t:
        if row[0] == "Player":
            if row[1] == 2:
              player = 2
        if row[0] == "":
            continue
        decks[player - 1].append(row[0])
    return decks



def play_rounds(p1, p2):
    while p1[0] > p2[0]:
        c1 = p1.pop(0)
        c2 = p2.pop(0)
        p1.extend([c1, c2])
        if len(p2) == 0:
            return
    while p2[0] > p1[0]:
        c1 = p1.pop(0)
        c2 = p2.pop(0)
        p2.extend([c2, c1])
        if len(p1) == 0:
            return


def calc_score(deck):
    score = 0
    for (i, d) in enumerate(reversed(deck)):
        score += d * (i + 1)
    return score

@e.part1()
def part1(xs):
    p1, p2 = xs
    p1, p2 = list(p1), list(p2)
    print(len(p1), len(p2))
    for r in range(100000):
        play_rounds(p1, p2)
        if len(p1) == 0:
            return calc_score(p2)
        elif len(p2) == 0:
            return calc_score(p1)

def hash_list(xs):
    h = 1234
    for x in xs:
        h ^= hash(x)
    return h


game_cache = {}

@e.part2()
def part2(xs):
    p1, p2 = xs
    previous_rounds = []
    _, cards = recursive_play(p1, p2)
    while True:
        if len(p1) == 0:
            return calc_score(p2)
        elif len(p2) == 0:
            return calc_score(p1)
        found_previous = False

        for r in previous_rounds:
            if r[0] == p1 and r[1] == p2:
                found_previous = True
        if found_previous:
            p1.extend([p1.pop(0), p2.pop(0)])
            continue

        previous_rounds.append((list(p1), list(p2)))

        c1 = p1.pop(0)
        c2 = p2.pop(0)
        winner = -1
        if c1 >= len(p1) and c2 >= len(p2):
            winner = recursive_play(list(p1), list(p2))
        else:
            if c1 > c2:
                winner = 1
            elif c2 > c2:
                winner = 2
        apply_winner(winner, p1, p2, c1, c2)


def apply_winner(winner, p1, p2, c1, c2):
    if winner == 1:
        p1.extend([c1, c2])
    elif winner == 2:
        p2.extend([c2, c1])
    else:
        assert False

def highest_card(c1, c2):
    if c1 > c2:
        return 1
    elif c2 > c1:
        return 2
    else:
        assert False


def recursive_play(p1, p2):
    seen = set()

    while len(p1) > 0 and len(p2) > 0:
        if (tuple(p1), tuple(p2)) in seen:
            return 1, p1
        seen.add((tuple(p1), tuple(p2)))
        c1 = p1.pop(0)
        c2 = p2.pop(0)
        winner = -1
        if len(p1) >= c1 and len(p2) >= c2:
            next_p1 = list(p1[:c1])
            next_p2 = list(p2[:c2])
            winner, _ = recursive_play(next_p1, next_p2)
        else:
            winner = highest_card(c1, c2)
        apply_winner(winner, p1, p2, c1, c2)
    winner = highest_card(len(p1), len(p2))
    return winner, p1 if winner == 1 else p2



e()
