from collections import defaultdict, deque

from aocd import data


maze = data.splitlines()
graph = defaultdict(list)
portals_by_point = {}
portals_by_name = defaultdict(list)
for y, row in enumerate(maze):
    for x, element in enumerate(row):
        if element == '.':
            for i, j in ((1,0), (0,1), (-1,0), (0,-1)):
                nx = x+i
                ny = y+j
                if maze[ny][nx] == '.':
                    graph[complex(x,y)].append(complex(nx,ny))
                elif maze[ny][nx].isalpha():
                    if i == 1:
                        name = maze[ny][nx] + maze[ny][nx+1]
                    elif i == -1:
                        name = maze[ny][nx-1] + maze[ny][nx]
                    elif j == 1:
                        name = maze[ny][nx] + maze[ny+1][nx]
                    elif j == -1:
                        name = maze[ny-1][nx] + maze[ny][nx]

                    portals_by_name[name].append(complex(x,y))
                    portals_by_point[complex(x,y)] = name

start = portals_by_name['AA'][0]
queue = deque([(start, 0)])
visited = set()
while queue:
    point, steps = queue.popleft()

    if point in portals_by_name['ZZ']:
        print('Part 1:', steps)
        break

    for new_point in graph[point]:
        if new_point not in visited:
            queue.append((new_point, steps+1))
            visited.add(new_point)

    portal = portals_by_point.get(point)
    if portal is not None:
        for new_point in portals_by_name[portal]:
            if new_point not in visited and new_point != point:
                queue.append((new_point, steps+1))
                visited.add(new_point)

start = portals_by_name['AA'][0]
queue = deque([(start, 0, 0)])
visited = set([start, 0])
while queue:
    point, level, steps = queue.popleft()

    if point in portals_by_name['ZZ'] and level == 0:
        print('Part 2:', steps)
        break

    for new_point in graph[point]:
        if (new_point, level) not in visited:
            queue.append((new_point, level, steps+1))
            visited.add((new_point, level))

    portal = portals_by_point.get(point)

    if portal is not None:
        if point.imag in (2, len(maze)-3) or point.real in (2, len(maze[0])-3):
            # outer portal
            new_level = -1
        else:
            # inner portal
            new_level = 1

        if level + new_level < 0:
            # ignore, already at outermost level
            continue

        for new_point in portals_by_name[portal]:
            if (new_point, level+new_level) not in visited and new_point != point:
                queue.append((new_point, level+new_level, steps+1))
                visited.add((new_point, level+new_level))
