from collections import defaultdict

from aocd import data

from p09 import Boost


class Cabinet(Boost):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.screen = defaultdict(int)
        self.x = None
        self.y = None
        self.score = None
        self.ball_x = 0
        self.paddle_x = 0

    def execute(self):
        while (code := self._get_op_code()).value != 99:
            arg1, arg2, arg3 = self._get_args(code)
            op = self._get_op(code.op)

            if code.op == 3:
                if self.paddle_x < self.ball_x:
                    op(arg1, 1)
                elif self.paddle_x > self.ball_x:
                    op(arg1, -1)
                else:
                    op(arg1, 0)
            elif code.op == 4:
                self.pointer += 2
                if self.x is None:
                    self.x = arg1.value
                elif self.y is None:
                    self.y = arg1.value
                else:
                    if self.x == -1 and self.y == 0:
                        self.score = arg1.value
                    else:
                        point = (self.x, self.y)
                        self.screen[point] = arg1.value
                        if arg1.value == 4:
                            self.ball_x = self.x
                        elif arg1.value == 3:
                            self.paddle_x = self.x

                    self.x = None
                    self.y = None
            else:
                op(arg1, arg2, arg3, None)


if __name__ == '__main__':
    program = [code for code in data.split(',')] + ['0']*10000
    cabinet = Cabinet(program)
    cabinet.execute()
    block_tiles = sum(tile == 2 for tile in cabinet.screen.values())
    print('Part 1:', block_tiles)

    # infinite money cheat code
    program[0] = '2'
    cabinet = Cabinet(program)
    cabinet.execute()
    print('Part 2:', cabinet.score)
