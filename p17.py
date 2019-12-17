from collections import defaultdict

from aocd import data

from intcode import Computer


class ASCII(Computer):
    pass


ascii = ASCII(data)
ascii.execute(None)
# print(ascii.output)
lines = []
from pprint import pprint
line = []
for i in ascii.output:
    if i != 10:
        line.append(i)
    else:
        lines.append(line.copy())
        line = []

# d = defaultdict(int)
s = 0
for y, line in enumerate(lines[:-1]):
    for x, c in enumerate(line):
        if c == 35:
            if x == len(line)-1 or x == 0 or y == len(lines)-1 or y == 0:
                continue
            # print(x, y)
            if lines[y][x-1] == lines[y][x+1] == lines[y-1][x] == lines[y+1][x]:
                s += x*y
                print(s)
                # pos = complex(x,y)
                # d[pos] += 1

# s = 0
# for p, i in d.items():
#     if i == 2:
#         s += p.real * p.imag

print(s)
