import re

from collections import deque

from aocd import data


DECK_SIZE_SMALL = 10_007
DECK_SIZE_BIG = 119_315_717_514_047
REPEATS = 101_741_582_076_661
CARD_NO = 2019
CARD_POS = 2020


def deal_new_stack(deck):
    deck.reverse()


def deal_cut(deck, n):
    deck.rotate(n*-1)


def deal_increment(deck, n):
    new_deck = deck.copy()

    for i, card in enumerate(deck):
        new_deck[i*n%len(deck)] = card

    return new_deck


p = re.compile(r'(\w+)\s(-?\d+)')
deck = deque(range(DECK_SIZE_SMALL))
increment_multiplier = 1
offset_difference = 0

for shuffle in data.splitlines():
    if 'new' in shuffle:
        deal_new_stack(deck)
        increment_multiplier = (increment_multiplier * -1) % DECK_SIZE_BIG
        offset_difference = (increment_multiplier + offset_difference) % DECK_SIZE_BIG
    else:
        shuffle_type, n = p.search(shuffle).groups()
        n = int(n)

        if shuffle_type == 'cut':
            deal_cut(deck, n)
            offset_difference = (offset_difference + (n * increment_multiplier)) % DECK_SIZE_BIG
        elif shuffle_type == 'increment':
            deck = deal_increment(deck, n)
            increment_multiplier = (increment_multiplier * pow(n, DECK_SIZE_BIG-2, DECK_SIZE_BIG)) % DECK_SIZE_BIG

print('Part 1:', deck.index(CARD_NO))

increment = pow(increment_multiplier, REPEATS, DECK_SIZE_BIG)
offset = offset_difference * (1 - increment) * pow((1 - increment_multiplier) % DECK_SIZE_BIG, DECK_SIZE_BIG-2, DECK_SIZE_BIG)
offset %= DECK_SIZE_BIG

card = (offset + CARD_POS * increment) % DECK_SIZE_BIG
print('Part 2:', card)
