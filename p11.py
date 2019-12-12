from collections import defaultdict

from aocd import data

from p09 import Boost


class Robot(Boost):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.hull = defaultdict(int)
        self.pos = 0j
        self.direction = 0
        self.need_color = True
        self.movement = {
            0: {0: (-1, 3), 1: (1, 1)},    # facing up, move left or right
            1: {0: (-1j, 0), 1: (1j, 2)},  # facing right, move up or down
            2: {0: (1, 1), 1: (-1, 3)},    # facing down, move right or left
            3: {0: (1j, 2), 1: (-1j, 0)},  # facing left, move down or up
        }

    def _move(self, rotation):
        travel, new_direction = self.movement[self.direction][rotation]
        self.direction = new_direction
        self.pos += travel

    def execute(self):
        while (code := self._get_op_code()).value != 99:
            arg1, arg2, arg3 = self._get_args(code)
            op = self._get_op(code.op)

            if code.op == 3:
                op(arg1, str(self.hull[self.pos]))
            elif code.op == 4:
                self.pointer += 2
                if self.need_color:
                    # paint current panel
                    self.hull[self.pos] = arg1.value
                    self.need_color = False
                else:
                    # get rotation for next position
                    # and then move to it
                    rotation = arg1.value
                    self._move(rotation)
                    self.need_color = True
            else:
                op(arg1, arg2, arg3, None)


if __name__ == '__main__':
    program = [code for code in data.split(',')] + ['0']*1000
    robot = Robot(program)
    robot.execute()
    print('Part 1:', len(robot.hull))

    robot = Robot(program)
    # initial starting panel
    # must be painted white
    robot.hull[robot.pos] = 1
    robot.execute()
    height = max(robot.hull.keys(), key=lambda p: p.imag).imag
    width = max(robot.hull.keys(), key=lambda p: p.real).real

    print('Part 2:')

    for y in range(int(height)+1):
        for x in range(int(width)+1):
            p = complex(x,y)
            if robot.hull[p] == 1:
                print('#', end='')
            else:
                print(' ', end='')
        print()
