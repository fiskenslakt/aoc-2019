from collections import defaultdict, deque

from aocd import data


def dfs(orbits, mass):
    if mass not in orbits:
        return 0

    n_orbits = 0
    for new_mass in orbits[mass]:
        n_orbits += 1 + dfs(orbits, new_mass)

    return n_orbits


def bfs(orbits, start_mass, end_mass):
    # offset orbital jumps to -2
    # to not count start and end mass
    queue = deque([(start_mass, -2)])
    seen = set([start_mass])

    while queue:
        mass, jumps = queue.popleft()

        if mass == end_mass:
            return jumps

        for new_mass in orbits[mass]:
            if new_mass in seen:
                continue

            queue.append((new_mass, jumps+1))
            seen.add(new_mass)


orbits = defaultdict(list)

for orbit in data.splitlines():
    orbiter, orbitee = orbit.split(')')
    orbits[orbiter].append(orbitee)

print('Part 1:', sum(dfs(orbits, mass) for mass in orbits))

for orbit in data.splitlines():
    orbiter, orbitee = orbit.split(')')
    orbits[orbitee].append(orbiter)

jumps = bfs(orbits, 'YOU', 'SAN')
print('Part 2:', jumps)
