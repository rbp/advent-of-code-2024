from collections import namedtuple
from time import sleep
import heapq
import sys


Point = namedtuple("Point", "x y".split())


def steps_after(bytes, n, side):
    map = mkmap(side)
    fall(map, bytes, n)
    show(map)
    return shortest_path(map)


def fall(map, bytes, n):
    for i in range(n):
        map[bytes[i].y][bytes[i].x] = "#"


def shortest_path(map):
    distances = mkmap(len(map), None)
    visited = set()

    start = Point(0, 0)
    end = Point(len(map) - 1, len(map) - 1)
    distances[end.x][end.y] = 0
    nodes = [(0, end)]
    iterations = 0
    while nodes:
        distance, node = heapq.heappop(nodes)
        if node in visited:
            continue
        neighbours = get_neighbours(map, node, visited)
        for neighbour in neighbours:
            distances[neighbour.x][neighbour.y] = distance + 1
            heapq.heappush(nodes, (distance + 1, neighbour))

        iterations += 1
        if iterations % 100 == 0:
            clear()
            show(map, visited, node)
            sleep(0.2)

        visited.add(node)
        if start in neighbours:
            break

    return distances[start.x][start.y]


def get_neighbours(map, point, visited):
    neighbours = []
    for x, y in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
        neighbour = Point(point.x + x, point.y + y)
        if not (
            0 <= neighbour.x < len(map) and 0 <= neighbour.y < len(map[neighbour.x])
        ):
            continue
        if map[neighbour.x][neighbour.y] == "#":
            continue
        if neighbour in visited:
            continue
        neighbours.append(neighbour)
    return neighbours


def mkmap(side, ch="."):
    return [[ch] * side for i in range(side)]


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


def read_point(s):
    parts = s.partition(",")
    return Point(int(parts[0]), int(parts[2]))


def read_bytes(f):
    return [read_point(row.strip()) for row in f.readlines()]


def main():
    infile = sys.argv[1]
    side = int(sys.argv[2])

    with open(infile) as f:
        bytes = read_bytes(f)

    print(f"Part 1: {steps_after(bytes, 1024 if side == 71 else 12, side)}")


if __name__ == "__main__":
    main()
