from aocd import data


directions = {'U': 1j, 'D': -1j,
              'L': -1, 'R': 1}


def lay_wire(layout):
    point = 0j
    steps = 0
    for instruction in layout:
        direction, amount = instruction[0], int(instruction[1:])
        for _ in range(amount):
            steps += 1
            point += directions[direction]
            yield point, steps


wire_a, wire_b = map(lambda wire: wire.split(','), data.splitlines())
points = {}
intersections = []
intersection_steps = []

for point, steps in lay_wire(wire_a):
    points[point] = steps

for point, steps in lay_wire(wire_b):
    if point in points:
        intersection_steps.append(steps + points[point])
        intersections.append(point)

point = min(intersections, key=lambda point: (abs(point.real), abs(point.imag)))
print('Part 1:', int(abs(point.real) + abs(point.imag)))
print('Part 2:', min(intersection_steps))
