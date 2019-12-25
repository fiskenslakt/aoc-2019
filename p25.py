from collections import deque

from aocd import data

from intcode import Computer


class Droid(Computer):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.queue = deque()

    def _op_4(self, *args, **kwargs):
        super()._op_4(*args, **kwargs)
        print(chr(self.output[-1]), end='')

    def execute(self):
        while (intcode := self._get_op_code()) != 99:
            args = self._get_args(intcode)
            op = self._get_op(intcode.op)
            if intcode.op == 3:
                if not self.queue:
                    print()
                    command = input('>')
                    for char in command:
                        self.queue.append(ord(char))
                    self.queue.append(10)
                op(args[0], None, None, self.queue.popleft(), modes=intcode.modes)
            else:
                op(*args, modes=intcode.modes)


droid = Droid(data)
droid.execute()
