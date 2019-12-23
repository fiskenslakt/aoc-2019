from itertools import cycle
from collections import deque

from aocd import data

from intcode import Computer


class NIC(Computer):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.queue = deque()

    def execute(self):
        while (intcode := self._get_op_code()) != 99:
            args = self._get_args(intcode)
            op = self._get_op(intcode.op)
            yield
            if intcode.op == 3:
                try:
                    packet = self.queue.popleft()
                except IndexError:
                    packet = -1
                op(*args, packet, modes=intcode.modes)
            else:
                op(*args, modes=intcode.modes)

nics = [(nic:=NIC(data), nic.execute()) for _ in range(50)]

for i, (nic, gnic) in enumerate(nics):
    gnic.send(None)
    nic.queue.append(i)

for nic, gnic in cycle(nics):
    if len(nic.output) == 3:
        address, x, y = nic.output
        if address == 255:
            print('Part 1:', y)
            break
        nic.output = []
        nics[address][0].queue.append(x)
        nics[address][0].queue.append(y)
    next(gnic)
