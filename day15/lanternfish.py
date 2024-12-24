from collections import namedtuple
from copy import deepcopy
from enum import Enum
import sys

Vector = namedtuple("Vector", "x y".split())
UP = Vector(-1, 0)
LEFT = Vector(0, -1)
DOWN = Vector(1, 0)
RIGHT = Vector(0, 1)


class Tile(Enum):
    ROBOT = "@"
    WALL = "#"
    OBST = "O"
    WIDE_OBST_LEFT = "["
    WIDE_OBST_RIGHT = "]"
    SPACE = "."


def total_coords(map, movements):
    perform_movements(map, movements)
    coords = calc_coords(map)

    return sum(coords)


def perform_movements(map, movements):
    robot = find_robot(map)
    for i, movement in enumerate(movements):
        moved_to = move(map, robot, movement)
        if moved_to:
            robot = moved_to

        print(f"Move {movement}:")
        show(map)
        print()


def move(map, pos, movement):
    next = next_pos(pos, movement)
    moved = None

    match map[next.x][next.y]:
        case Tile.SPACE.value:
            map[next.x][next.y] = map[pos.x][pos.y]
            map[pos.x][pos.y] = Tile.SPACE.value
            moved = next
        case Tile.OBST.value:
            moved = move(map, next, movement)
            if moved:
                moved = move(map, pos, movement)
        case Tile.WALL.value:
            # This is just here for clarity. If we can't move, we don't
            pass
        case _:
            raise ValueError(
                f"Invalid movement: {map[next.x][next.y]} @{next.x},{next.y} -> {movement}"
            )
    return moved


def next_pos(position, movement):
    return Vector(position.x + movement.x, position.y + movement.y)


def calc_coords(map):
    for i, row in enumerate(map):
        for j, col in enumerate(row):
            if col == Tile.OBST.value:
                yield 100 * i + j


def find_robot(map):
    for i, row in enumerate(map):
        for j, col in enumerate(row):
            if col == Tile.ROBOT.value:
                return Vector(i, j)
    raise ValueError("cannot find robot")


def show(map):
    for line in map:
        print("".join(line))


def read_input(f):
    vector = {"^": UP, "<": LEFT, "v": DOWN, ">": RIGHT}

    map = []
    movements = []
    line = f.readline().strip()
    while line != "":
        map.append(list(line))
        line = f.readline().strip()

    movements = [vector[c] for line in f.read().splitlines() for c in line]
    return map, movements


def main():
    infile = sys.argv[1]

    with open(infile) as f:
        map, movements = read_input(f)

    show(map)
    print(f"Part 1: {total_coords(deepcopy(map), movements)}")


if __name__ == "__main__":
    main()
