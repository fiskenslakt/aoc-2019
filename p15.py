from collections import defaultdict, deque
from itertools import cycle

from aocd import data

from intcode import Computer


NORTH = 1
SOUTH = 2
WEST = 3
EAST = 4


class RepairDroid(Computer):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.pos = 0j
        self.ship = defaultdict(str)
        self.visited = set()

    def _op_4(self, *args, modes):
        register = self._read(args[0], modes[0])
        self.pointer += 2
        return register

    def display_map(self):
        min_x = min(self.ship, key=lambda p: p.real).real
        max_x = max(self.ship, key=lambda p: p.real).real
        min_y = min(self.ship, key=lambda p: p.imag).imag
        max_y = max(self.ship, key=lambda p: p.imag).imag

        for y in range(int(min_y), int(max_y)+1):
            for x in range(int(min_x), int(max_x)+1):
                p = complex(x, y)
                if p == self.pos:
                    print('D', end='')
                elif self.ship[p] == '#':
                    print('#', end='')
                elif p == self.oxygen_system:
                    print('O', end='')
                else:
                    print(' ', end='')
            print()

    def execute(self):
        while (intcode := self._get_op_code()) != 99:
            args = self._get_args(intcode)
            op = self._get_op(intcode.op)
            if intcode.op == 3:
                command = yield
                op(*args, command, modes=intcode.modes)
            elif intcode.op == 4:
                yield op(*args, modes=intcode.modes)
            else:
                op(*args, modes=intcode.modes)


def move_droid(repair_droid, command, move):
    old_pos = repair_droid.pos
    new_pos = repair_droid.pos + move
    status = droid.send(command)  # send command and get status
    next(droid)                   # get ready for next command input

    if status == 0:
        repair_droid.ship[new_pos] = '#'
    elif status == 1:
        repair_droid.pos += move
        if repair_droid.ship[repair_droid.pos] == '.':
            repair_droid.visited.add(old_pos)
        repair_droid.ship[new_pos] = '.'
    elif status == 2:
        repair_droid.oxygen_system = new_pos
        repair_droid.pos += move
        if repair_droid.ship[repair_droid.pos] == '.':
            repair_droid.visited.add(old_pos)
        repair_droid.ship[new_pos] = '.'

    return status


up_down = cycle([(1, -1j), (2, 1j)])
left_right = cycle([(3, -1), (4, 1)])
repair_droid = RepairDroid(data)
droid = repair_droid.execute()
droid.send(None)  # initialize droid

command_y, move_y = next(up_down)
command_x, move_x = next(left_right)
last_move = WEST
last_status = 1
# follow walls until we can't move
# if both x and y direction fail -> deadend or inside corner
# if both x and y direction succeed -> moving around corner
while True:
    new_y = move_y + repair_droid.pos
    new_x = move_x + repair_droid.pos
    if last_move in (WEST, EAST) and new_y not in repair_droid.visited:  # move north/south
        status = move_droid(repair_droid, command_y, move_y)
        if bool(status) == bool(last_status):
            command_x, move_x = next(left_right)

        last_move = command_y
        last_status = status
        continue

    if last_move in (NORTH, SOUTH) and new_x not in repair_droid.visited:  # move west/east
        status = move_droid(repair_droid, command_x, move_x)
        if bool(status) == bool(last_status):
            command_y, move_y = next(up_down)

        last_move = command_x
        last_status = status
    else:
        break

# find shortest path to oxygen system
queue = deque([(0j, 0)])
visited = set()
while queue:
    pos, steps = queue.popleft()

    if pos == repair_droid.oxygen_system:
        print('Part 1:', steps)
        break

    for p in (1, -1, 1j, -1j):
        new_pos = pos + p
        if repair_droid.ship[new_pos] == '.' and new_pos not in visited:
            queue.append((new_pos, steps+1))
            visited.add(new_pos)

# find minutes till room is full of oxygen
queue = deque([repair_droid.oxygen_system])
visited = set()
minutes = -1  # avoid off by 1
while queue:
    size = len(queue)
    for _ in range(size):
        pos = queue.popleft()

        for p in (1, -1, 1j, -1j):
            new_pos = pos + p
            if repair_droid.ship[new_pos] == '.' and new_pos not in visited:
                queue.append(new_pos)
                visited.add(new_pos)
    minutes += 1

print('Part 2:', minutes)
