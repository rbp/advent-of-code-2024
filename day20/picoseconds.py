from copy import deepcopy
from collections import namedtuple
import heapq
import sys
from time import sleep

Point = namedtuple("Point", "x y".split())


def cheats(map, save_ge=1):
    start, end = find_extremities(map)
    distances = shortest_path(map, start, end)

    savers = 0
    for wall, gain in cheatable_walls(map, distances):
        # It's better to calculate the gain, not try to map all distances again
        # map[wall.x][wall.y] = "."
        # d = shortest_path(map, start, end)
        # gain = distances[start.x][start.y] - d[start.x][start.y]
        if gain >= save_ge:
            savers += 1
        map[wall.x][wall.y] = "#"

    return savers


def shortest_path(map, start, end):
    distances = mkmap(map, None)
    visited = set()

    distances[end.x][end.y] = 0
    nodes = [(0, end)]
    while nodes:
        distance, node = heapq.heappop(nodes)
        if node in visited:
            continue
        neighbours = get_neighbours(map, node, visited)
        for neighbour in neighbours:
            distances[neighbour.x][neighbour.y] = distance + 1
            heapq.heappush(nodes, (distance + 1, neighbour))

        visited.add(node)
        if start in neighbours:
            break
        # clear()
        # show(map, visited, node)
        # sleep(0.05)

    return distances


def cheatable_walls(map, distances):
    """Yiels a wall and how much distance in gained by removing it"""
    for i in range(1, len(map) - 1):
        for j in range(1, len(map[i]) - 1):
            if map[i][j] != "#":
                continue
            # It's a cheatable wall if removing it connects 2 parts of the path
            wall = Point(i, j)
            neighbours = get_neighbours(map, wall, {})
            if len(neighbours) < 2:
                continue
            yield wall, gain_crossing_wall(wall, neighbours, distances)


def gain_crossing_wall(wall, neighbours, distances):
    gains = set()
    for neighbour in neighbours:
        for other in neighbours:
            if neighbour == other:
                continue
            gains.add(
                abs(distances[neighbour.x][neighbour.y] - distances[other.x][other.y])
                - 2
            )

    return max(gains)


def get_neighbours(map, point, visited):
    neighbours = []
    for x, y in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
        neighbour = Point(point.x + x, point.y + y)
        if not valid_pos(map, neighbour) or neighbour in visited:
            continue
        neighbours.append(neighbour)
    return neighbours


def valid_pos(map, pos):
    return (0 <= pos.x < len(map) and 0 <= pos.y < len(map[pos.x])) and map[pos.x][
        pos.y
    ] != "#"


def find_extremities(map):
    start = end = None
    for i in range(len(map)):
        for j in range(len(map[i])):
            if map[i][j] == "S":
                start = Point(i, j)
            elif map[i][j] == "E":
                end = Point(i, j)
            if start is not None and end is not None:
                return start, end


def mkmap(template, fill):
    return [[fill] * len(row) for row in template]


def show(map, visited=None, node=None):
    for i in range(len(map)):
        for j in range(len(map[i])):
            if node and (i, j) == node:
                ch = boldgreen("*")
            elif visited and (i, j) in visited:
                ch = boldred("O")
            else:
                ch = map[i][j]
            print(ch, end="")
        print()


def boldred(s):
    start = "\033[1;31m"
    end = "\033[0;0m"
    return f"{start}{s}{end}"


def boldgreen(s):
    start = "\033[1;32m"
    end = "\033[0;0m"
    return f"{start}{s}{end}"


def clear():
    print(chr(27) + "[2J")


def read_map(f):
    return [list(row.strip()) for row in f.readlines()]


def main():
    infile = sys.argv[1]
    with open(infile) as f:
        map = read_map(f)

    print(f"Part 1: {cheats(map, save_ge=100)}")


if __name__ == "__main__":
    main()
