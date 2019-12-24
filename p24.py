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

print(bio)
