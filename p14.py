import re

from math import ceil
from collections import defaultdict, deque

from aocd import data


CARGO = int(1e12)


class Chemical:
    def __init__(self, name: str, amount: int):
        self.name = name
        self.amount = amount

    def __repr__(self):
        return f'Chemical("{self.amount} {self.name}")'

    def __eq__(self, other):
        return self.name == other

    def __hash__(self):
        return hash(self.name)

    @classmethod
    def from_string(cls, chemical):
        amount, name = chemical.split()
        return cls(name, int(amount))


def get_ore(reactions, nfuel):
    queue = deque([(Chemical('FUEL', 1), nfuel)])
    surplus = defaultdict(int)
    ore_needed = 0

    while queue:
        chemical, needed = queue.popleft()

        if chemical == 'ORE':
            ore_needed += needed
            continue

        produced = next(c.amount for c in reactions if c == chemical)

        if surplus[chemical.name] > 0:
            needed -= surplus[chemical.name]
            surplus[chemical.name] = 0

        multiple = ceil(needed/produced)
        surplus[chemical.name] += produced*multiple - needed

        for input_chemical in reactions[chemical]:
            queue.append((input_chemical, input_chemical.amount*multiple))

    return ore_needed


p = re.compile(r'\d+\s\w+')
reactions = {}

for reaction in data.splitlines():
    *input_chemicals, output_chemical = p.findall(reaction)
    output = Chemical.from_string(output_chemical)
    inputs = [Chemical.from_string(chemical) for chemical in input_chemicals]
    reactions[output] = inputs

ores_needed = get_ore(reactions, 1)

print('Part 1:', ores_needed)

left = 1
right = CARGO
while left + 1 < right:
    mid = (left + right) // 2
    ores = get_ore(reactions, mid)

    if ores > CARGO:
        right = mid
    elif ores < CARGO:
        left = mid

if get_ore(reactions, right) < CARGO:
    fuel = right
else:
    fuel = left

print('Part 2:', fuel)
