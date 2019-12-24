from collections import defaultdict

from aocd import data


grid = data.splitlines()
states = {hash(data)}

while True:
    new_grid = []
    for y, row in enumerate(grid):
        new_row = ''
        for x, col in enumerate(row):
            bugs = 0
            for i, j in ((0,1),(1,0),(0,-1),(-1,0)):
                nx, ny = x+i, y+j

                if nx < 0 or nx > 4:
                    continue
                if ny < 0 or ny > 4:
                    continue

                if grid[ny][nx] == '#':
                    bugs += 1

            if grid[y][x] == '#':
                if bugs == 1:
                    new_row += '#'
                else:
                    new_row += '.'

            elif grid[y][x] == '.':
                if bugs in (1, 2):
                    new_row += '#'
                else:
                    new_row += '.'

        new_grid.append(new_row)

    eres = '\n'.join(new_grid)
    if hash(eres) in states:
        bio = 0
        for i,e in enumerate(''.join(new_grid)):
            if e == '#':
                bio += 2**i
        break
    else:
        states.add(hash(eres))
        grid = new_grid.copy()

print('Part 1:', bio)


def new_grid():
    return [['.']*5 for _ in range(5)]


grid = list(map(list, data.splitlines()))
levels = defaultdict(new_grid)
levels[0] = grid

for _ in range(200):
    min_level = min(levels)
    max_level = max(levels)
    levels[min_level-1]
    levels[max_level+1]
    new_grids = {}
    for level, grid in list(levels.items()):
        new_grid = []
        for y, row in enumerate(grid):
            new_row = []
            for x, col in enumerate(row):
                if (x,y) == (2,2):
                    new_row.append('.')
                    continue
                bugs = 0
                for i, j in ((0,1),(1,0),(0,-1),(-1,0)):
                    nx, ny = x+i, y+j

                    # recurse inward
                    if (nx, ny) == (2, 2):
                        if (x, y) == (2, 1):
                            for cell in levels[level+1][0]:
                                bugs += 1 if cell == '#' else 0
                        elif (x, y) == (1, 2):
                            for row in levels[level+1]:
                                bugs += 1 if row[0] == '#' else 0
                        elif (x, y) == (3, 2):
                            for row in levels[level+1]:
                                bugs += 1 if row[-1] == '#' else 0
                        elif (x, y) == (2, 3):
                            for cell in levels[level+1][-1]:
                                bugs += 1 if cell == '#' else 0

                    # recurse outward
                    if nx < 0 and levels[level-1][2][1] == '#':
                        bugs += 1
                    elif nx > 4 and levels[level-1][2][3] == '#':
                        bugs += 1
                    elif ny < 0 and levels[level-1][1][2] == '#':
                        bugs += 1
                    elif ny > 4 and levels[level-1][3][2] == '#':
                        bugs += 1
                    else:
                        if nx < 0 or nx > 4 or ny < 0 or ny > 4:
                            continue
                        # normal neighbor
                        elif grid[ny][nx] == '#':
                            bugs += 1

                if grid[y][x] == '#':
                    if bugs == 1:
                        new_row.append('#')
                    else:
                        new_row.append('.')
                elif bugs in (1, 2):
                    new_row.append('#')
                else:
                    new_row.append('.')

            new_grid.append(new_row)
        new_grids[level] = new_grid
    for level, grid in new_grids.items():
        levels[level] = grid.copy()

bugs = sum(col == '#' for grid in levels.values() for row in grid for col in row)
print('Part 2:', bugs)
