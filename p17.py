from aocd import data

from intcode import Computer


class ASCII(Computer):
    def execute(self, instructions):
        while (intcode := self._get_op_code()) != 99:
            args = self._get_args(intcode)
            op = self._get_op(intcode.op)
            if intcode.op == 3:
                op(*args, next(instructions), modes=intcode.modes)
            else:
                op(*args, modes=intcode.modes)


ascii = ASCII(data)
ascii.execute(None)

lines = []
line = []
for i in ascii.output:
    if i != 10:
        line.append(i)
    else:
        lines.append(line.copy())
        line = []

s = 0
for y, line in enumerate(lines[:-1]):
    for x, c in enumerate(line):
        if c == 35:
            if x == len(line)-1 or x == 0 or y == len(lines)-1 or y == 0:
                continue
            if lines[y][x-1] == lines[y][x+1] == lines[y-1][x] == lines[y+1][x]:
                s += x*y

print('Part 1:', s)

# for line in lines:
#     for c in line:
#         print(chr(c), end='')
#     print()

ascii = ASCII(data)
ascii.memory[0] = 2
# bot = ascii.execute(None)
# initialize bot
# breakpoint()
# bot.send(None)

# path written out by hand
# R,10,L,8,R,10,R,4,L,6,L,6,R,10,R,10,L,8,R,10,R,4,L,6,R,12,R,12,R,10,L,6,L,6,R,10,L,6,R,12,R,12,R,10,R,10,L,8,R,10,R,4,L,6,L,6,R,10,R,10,L,8,R,10,R,4,L,6,R,12,R,12,R,10

A = 'L,6,L,6,R,10'
B = 'R,10,L,8,R,10,R,4'
C = 'L,6,R,12,R,12,R,10'
main = 'B,A,B,C,A,C,B,A,B,C'

instructions = [ord(i) for i in f'{main}\n{A}\n{B}\n{C}\nn\n']
ascii.execute(iter(instructions))
print('Part 2:', ascii.output[-1])
