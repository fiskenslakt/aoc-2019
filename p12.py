import re
from itertools import combinations
from math import gcd

from aocd import data


# data = '''<x=-1, y=0, z=2>
# <x=2, y=-10, z=-7>
# <x=4, y=-8, z=8>
# <x=3, y=5, z=-1>'''


class Moon:
    def __init__(self, x, y, z):
        self.x = int(x)
        self.y = int(y)
        self.z = int(z)
        self.vx = 0
        self.vy = 0
        self.vz = 0

    def __repr__(self):
        return f'Moon({self.x}, {self.y}, {self.z})'

    def __eq__(self, other):
        if moon.x != other.x:
            return False
        elif moon.y != other.y:
            return False
        elif moon.z != other.z:
            return False
        else:
            return True


def sim(moons):
    for m1, m2 in combinations(moons, 2):
        if m1.x < m2.x:
            m1.vx += 1
            m2.vx -= 1
        elif m1.x > m2.x:
            m1.vx -= 1
            m2.vx += 1

        if m1.y < m2.y:
            m1.vy += 1
            m2.vy -= 1
        elif m1.y > m2.y:
            m1.vy -= 1
            m2.vy += 1

        if m1.z < m2.z:
            m1.vz += 1
            m2.vz -= 1
        elif m1.z > m2.z:
            m1.vz -= 1
            m2.vz += 1

    for moon in moons:
        moon.x += moon.vx
        moon.y += moon.vy
        moon.z += moon.vz


moons = [Moon(*re.findall(r'-?\d+', moon)) for moon in data.splitlines()]

for step in range(1000):
    sim(moons)

pot = 0
kin = 0
energy = 0

for moon in moons:
    pot += abs(moon.x) + abs(moon.y) + abs(moon.z)
    kin += abs(moon.vx) + abs(moon.vy) + abs(moon.vz)
    energy += pot*kin
    pot = kin = 0

print('Part 1:', energy)

moons = [Moon(*re.findall(r'-?\d+', moon)) for moon in data.splitlines()]

x_fstate = tuple(moon.x for moon in moons)
y_fstate = tuple(moon.y for moon in moons)
z_fstate = tuple(moon.z for moon in moons)
x = y = z = True

for period in range(1, 10000000):
    x_state = tuple(moon.x for moon in moons)
    y_state = tuple(moon.y for moon in moons)
    z_state = tuple(moon.z for moon in moons)

    sim(moons)
    if x_state == x_fstate and x and all(moon.vx == 0 for moon in moons):
        # print(period, 'x')
        x_period = period
        x = False
    if y_state == y_fstate and y and all(moon.vy == 0 for moon in moons):
        # print(period, 'y')
        y_period = period
        y = False
    if z_state == z_fstate and z and all(moon.vz == 0 for moon in moons):
        # print(period, 'z')
        z_period = period
        z = False

    if x == y == z == False:
        break

xy_lcm = (x_period*y_period)//gcd(x_period,y_period)
xyz_lcm = (xy_lcm*z_period)//gcd(xy_lcm,z_period)
print('Part 2:', xyz_lcm)
