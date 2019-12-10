from math import atan2, degrees, hypot
from heapq import heappush, heappop
from collections import defaultdict

from aocd import data


asteroids = []
for y, row in enumerate(data.splitlines()):
    for x, col in enumerate(row):
        if col == '#':
            asteroids.append(complex(x,y))

detected = 0
monitoring_station = None
for a1 in asteroids:
    slopes = set()

    for a2 in asteroids:
        if a1 == a2:
            continue

        x = a2.real-a1.real
        y = a2.imag-a1.imag

        slopes.add(atan2(y,x))

    if len(slopes) > detected:
        detected = len(slopes)
        monitoring_station = a1

print('Part 1:', detected)

get_angle = lambda x1,y1,x2,y2: (degrees(atan2(y1-y2,x1-x2))-90) % 360
x1, y1 = monitoring_station.real, monitoring_station.imag
angles = defaultdict(list)
for asteroid in asteroids:
    if asteroid == monitoring_station:
        continue
    x2, y2 = asteroid.real, asteroid.imag
    angle = get_angle(x1,y1,x2,y2)
    dist = hypot(x2-x1, y2-y1)
    heappush(angles[angle], (dist, asteroid))

i = 1
for angle, distances in sorted(angles.items()):
    _, asteroid = heappop(distances)
    if i == 200:
        print('Part 2:', int(asteroid.real*100 + asteroid.imag))
    i += 1
