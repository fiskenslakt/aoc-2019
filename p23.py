from itertools import cycle
from collections import deque

from aocd import data

from intcode import Computer


class NIC(Computer):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.queue = deque()
        self.idle = False

    def execute(self):
        while (intcode := self._get_op_code()) != 99:
            args = self._get_args(intcode)
            op = self._get_op(intcode.op)
            yield
            if intcode.op == 3:
                try:
                    packet = self.queue.popleft()
                    self.idle = False
                except IndexError:
                    packet = -1
                    self.idle = True
                op(*args, packet, modes=intcode.modes)
            else:
                op(*args, modes=intcode.modes)


nics = [(nic:=NIC(data), nic.execute()) for _ in range(50)]
natx = None
naty = None
lastnaty = None
part1 = True

for i, (nic, gnic) in enumerate(nics):
    gnic.send(None)
    nic.queue.append(i)

for i, (nic, gnic) in enumerate(cycle(nics)):
    if i%50==49 and all(nic.idle for nic, _ in nics) and natx is not None:
        nics[0][0].idle = False

        if lastnaty == naty:
            print('Part 2:', naty)
            break

        nics[0][0].queue.append(natx)
        nics[0][0].queue.append(naty)
        lastnaty = naty

    if len(nic.output) == 3:
        address, x, y = nic.output

        if address == 255:
            nic.output = []
            natx = x
            naty = y

            if part1:
                print('Part 1:', y)
                part1 = False
            next(gnic)
            continue

        nic.output = []
        nics[address][0].queue.append(x)
        nics[address][0].queue.append(y)

    next(gnic)
