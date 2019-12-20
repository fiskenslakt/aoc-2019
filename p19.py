from itertools import count

from aocd import data

from intcode import Computer


class Drone(Computer):
    def execute(self, input_):
        while (intcode := self._get_op_code()) != 99:
            args = self._get_args(intcode)
            op = self._get_op(intcode.op)
            if intcode.op == 3:
                xy = next(input_)
                op(*args, xy, modes=intcode.modes)
            else:
                op(*args, modes=intcode.modes)


drone = Drone(data)
beam = 0
for y in count():
    if y == 50:
        print('Part 1:', beam)
        break
    x_count = count()
    found_beam = False
    for x in x_count:
        drone.execute(iter([x, y]))
        output = drone.output[-1]
        drone.reset()
        if output == 1:
            beam += 1
            found_beam = True
        elif found_beam or x > 49:
            break
