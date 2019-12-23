from collections import deque

from aocd import data


def key_index(key):
    return ord(key)-97


def has_key(mask, key):
    return mask & (1 << key_index(key)) != 0


def add_key(mask, key):
    return mask | (1 << key_index(key))


maze = data.splitlines()
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
