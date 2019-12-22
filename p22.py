import re

from collections import deque

from aocd import data


def new_stack(deck):
    deck.reverse()


def cut(deck, n):
    deck.rotate(n*-1)


def increment(deck, n):
    new_deck = deck.copy()

    for i, card in enumerate(deck):
        new_deck[i*n%len(deck)] = card

    return new_deck


p = re.compile(r'(\w+)\s(-?\d+)')
deck = deque(range(10_007))

for shuffle in data.splitlines():
    if 'new' in shuffle:
        new_stack(deck)
    else:
        shuffle_type, n = p.search(shuffle).groups()
        n = int(n)

        if shuffle_type == 'cut':
            cut(deck, n)
        elif shuffle_type == 'increment':
            deck = increment(deck, n)

print('Part 1:', deck.index(2019))
