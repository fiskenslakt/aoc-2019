from aocd import data
from collections import defaultdict, deque

def dfs(orbits, obj):
    if obj not in orbits:
        return 0
    n = 0
    for new_obj in orbits[obj]:
        n += 1 + dfs(orbits, new_obj)

    return n


orbits = defaultdict(list)

for line in data.splitlines():
    a, b = line.split(')')
    orbits[a].append(b)

print(sum(dfs(orbits, obj) for obj in orbits))

orbits = defaultdict(list)

for line in data.splitlines():
    a, b = line.split(')')
    orbits[a].append(b)
    orbits[b].append(a)

q = deque([('YOU', -2)])
n = 0
seen = set()
while q:
    size = len(q)
    for _ in range(size):
        obj, n = q.popleft()
        seen.add(obj)

        if obj == 'SAN':
            print(n)
            raise SystemExit

        for nobj in orbits[obj]:
            if nobj in seen:
                continue
            q.append((nobj, n+1))
            seen.add(nobj)

print(n)

