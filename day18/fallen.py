from collections import namedtuple
from time import sleep
import heapq
import sys


Point = namedtuple("Point", "x y".split())


def steps_after(bytes, n, side):
    map = mkmap(side)
    fall(map, bytes, n)
    show(map)
    distances = shortest_path(map)
    return distances


def fall_until_blocked(distances, bytes, initial_fall, side):
    map = mkmap(side)
    # We know from part 1 that we can fall at least these bytes
    fall(map, bytes, initial_fall)

    possible_path = path_from_distances(map, distances)
    for i in range(initial_fall, len(bytes)):
        fall_byte(map, bytes[i])
        if can_traverse(map, possible_path):
            # Actually, we just need to check if the latest fallen byte is in the path...
            # But fine. This is fast enough.
            continue
        distances = shortest_path(map)
        if distances[0][0] is None:
            return f"{bytes[i].x},{bytes[i].y}"
        possible_path = path_from_distances(map, distances)
        show(map)
    return shortest_path(map)


def fall(map, bytes, n):
    for i in range(n):
        map[bytes[i].y][bytes[i].x] = "#"


def fall_byte(map, byte):
    map[byte.y][byte.x] = "#"


def path_from_distances(map, distances):
    start = Point(0, 0)
    end = Point(len(map) - 1, len(map) - 1)
    node = start
    visited = {node}
    path = [node]
    while node != end:
        distance = distances[node.x][node.y]
        neighbours = [
            p
            for p in get_neighbours(map, node, visited)
            if distances[p.x][p.y] == distance - 1
        ]
        node = min(neighbours, key=lambda p: (end.x - p.x) ** 2 + (end.y - p.y) ** 2)
        visited.add(node)
        path.append(node)
    return path


def can_traverse(map, path):
    end = Point(len(map) - 1, len(map) - 1)
    i = 0
    while i < len(path):
        node = path[i]
        if not valid_pos(map, node):
            break

        if node == end:
            # clear()
            # show(map, path, node)
            # sleep(0.1)
            return True
        i += 1
    return False


def shortest_path(map):
    distances = mkmap(len(map), None)
    visited = set()

    start = Point(0, 0)
    end = Point(len(map) - 1, len(map) - 1)
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

    return distances


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

    fallen_bytes = 1024 if side == 71 else 12
    distances = steps_after(bytes, fallen_bytes, side)
    print(f"Part 1: {distances[0][0]}")
    print(f"Part 2: {fall_until_blocked(distances, bytes, fallen_bytes, side)}")


if __name__ == "__main__":
    main()
