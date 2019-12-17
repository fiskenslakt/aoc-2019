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

print('Part 1:', ''.join(str(digit) for digit in signal[:8]))

signal = [int(digit) for digit in data] * 10_000
offset = int(data[:7])
signal = signal[offset:]

for phase in range(PHASES):
    # every digit before offset is
    # multiplied by zero
    partial_sum = sum(signal)
    for position in range(len(signal)):
        # store value to remove from sum
        # as we're about to change it
        old_value = signal[position]
        signal[position] = partial_sum % 10
        # current digit will be multiplied by zero
        # in next theoretical part of the pattern
        # so we just remove it from the sum
        partial_sum -= old_value

print('Part 2:', ''.join(str(digit) for digit in signal[:8]))
