from collections import Counter

from aocd import data


lower, upper = map(int, data.split('-'))
strict = 0
very_strict = 0

for n in range(lower, upper+1):
    password = str(n)
    frequencies = Counter(password)

    if not all(int(i) <= int(j) for i, j in zip(password, password[1:])):
        continue

    if max(frequencies.values()) > 1:
        strict += 1
    else:
        continue

    if 2 in frequencies.values():
        very_strict += 1

print('Part 1:', strict)
print('Part 2:', very_strict)
