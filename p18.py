from collections import deque

from aocd import data


def key_index(key):
    return ord(key)-97


def has_key(mask, key):
    return mask & (1 << key_index(key)) != 0


def add_key(mask, key):
    return mask | (1 << key_index(key))


maze = list(map(list, data.splitlines()))
keys = set()

for y, row in enumerate(maze):
    for x, col in enumerate(row):
        if col == '@':
            start = (x, y)
        elif col.islower():
            keys.add(col)

visited = set([(start, 0)])
queue = deque([(start, 0, 0)])
while queue:
    (x, y), dist, mask = queue.popleft()

    if all(has_key(mask, key) for key in keys):
        print('Part 1:', dist)
        break

    for i, j in ((1,0), (0,1), (-1,0), (0,-1)):
        nx, ny = x+i, y+j
        new_pos = (nx, ny)
        if (new_pos, mask) in visited:
            continue

        if maze[ny][nx] in ('.', '@'):
            queue.append((new_pos, dist+1, mask))
            visited.add((new_pos, mask))
        elif maze[ny][nx].isupper():
            door = maze[ny][nx]
            key = door.lower()
            if has_key(mask, key):
                queue.append((new_pos, dist+1, mask))
                visited.add((new_pos, mask))
        elif maze[ny][nx].islower():
            key = maze[ny][nx]
            new_mask = add_key(mask, key)
            queue.append((new_pos, dist+1, new_mask))
            visited.add((new_pos, new_mask))


def bfs(source, keys):
    visited = set([(source, 0)])
    queue = deque([(source, 0, 0)])

    while queue:
        (x, y), dist, mask = queue.popleft()

        if all(has_key(mask, key) for key in keys):
            return dist

        for i, j in ((1,0), (0,1), (-1,0), (0,-1)):
            nx, ny = x+i, y+j
            new_pos = (nx, ny)

            if (new_pos, mask) in visited:
                continue

            if maze[ny][nx] in ('.', '@') or maze[ny][nx].isupper():
                queue.append((new_pos, dist+1, mask))
                visited.add((new_pos, mask))
            elif maze[ny][nx].islower():
                key = maze[ny][nx]
                new_mask = add_key(mask, key)
                queue.append((new_pos, dist+1, new_mask))
                visited.add((new_pos, new_mask))


sx, sy = start
maze[sy][sx-1] = '#'
maze[sy][sx+1] = '#'
maze[sy][sx]   = '#'
maze[sy-1][sx] = '#'
maze[sy+1][sx] = '#'

tlq_pos = (sx-1, sy-1)  # top left quadrant
trq_pos = (sx+1, sy-1)  # top right quadrant
blq_pos = (sx-1, sy+1)  # bottom left quadrant
brq_pos = (sx+1, sy+1)  # bottom right quadrant

tlq_keys = []
trq_keys = []
blq_keys = []
brq_keys = []

for y, row in enumerate(maze):
    for x, col in enumerate(row):
        if col.islower():
            if x < sx and y < sy:
                tlq_keys.append(col)
            elif x > sx and y < sy:
                trq_keys.append(col)
            elif x < sx and y > sy:
                blq_keys.append(col)
            elif x > sx and y > sy:
                brq_keys.append(col)

tlq_steps = bfs(tlq_pos, tlq_keys)
trq_steps = bfs(trq_pos, trq_keys)
blq_steps = bfs(blq_pos, blq_keys)
brq_steps = bfs(brq_pos, brq_keys)

steps = tlq_steps + trq_steps + blq_steps + brq_steps
print('Part 2:', steps)
