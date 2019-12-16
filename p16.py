from itertools import cycle

from aocd import data


PHASES = 100
PATTERN = (0, 1, 0, -1)

signal = [int(digit) for digit in data]

for phase in range(PHASES):
    new_signal = ''
    for position in range(1, len(data)+1):
        pattern = cycle([i for i in PATTERN for _ in range(position)])
        next(pattern)
        digit = 0
        for element, value in zip(signal, pattern):
            digit += element*value

        new_signal += str(digit)[-1]

    signal = [int(digit) for digit in new_signal]

print(''.join(str(digit) for digit in signal[:8]))
