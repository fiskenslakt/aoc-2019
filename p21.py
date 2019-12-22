from aocd import data

from intcode import Computer


class SpringDroid(Computer):
    def display(self):
        for i in self.output:
            print(chr(i), end='')

    def execute(self, instructions):
        instructions = map(ord, instructions)
        while (intcode := self._get_op_code()) != 99:
            args = self._get_args(intcode)
            op = self._get_op(intcode.op)
            if intcode.op == 3:
                op(*args, next(instructions), modes=intcode.modes)
            else:
                op(*args, modes=intcode.modes)


droid = SpringDroid(data)
instructions = 'OR C T\nOR A J\nAND J T\nNOT T J\nAND D J\nWALK\n'
droid.execute(instructions)
print('Part 1:', droid.output[-1])

droid.reset()
instructions = 'NOT C T\nNOT B J\nOR T J\nAND H J\nNOT A T\nOR T J\nAND D J\nRUN\n'
droid.execute(instructions)
print('Part 2:', droid.output[-1])
