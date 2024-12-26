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
    # show(map)
    # print()

    perform_movements(map, movements)
    coords = calc_coords(map)

    return sum(coords)


def perform_movements(map, movements):
    robot = find_robot(map)

    for movement in movements:
        moved_to = move(map, robot, movement)
        if moved_to:
            robot = moved_to

        # print(f"Move {movement}:")
        # show(map)
        # print()


def move(map, pos, movement):
    next = next_pos(pos, movement)
    moved = None

    match map[next.x][next.y]:
        case Tile.SPACE.value:
            moved = do_move(map, pos, movement)
        case Tile.OBST.value | Tile.WIDE_OBST_LEFT.value | Tile.WIDE_OBST_RIGHT.value:
            if can_move(map, pos, movement):
                moved = do_move(map, pos, movement)
        case Tile.WALL.value:
            # This is just here for clarity. If we can't move, we don't
            pass
        case _:
            raise ValueError(
                f"Invalid movement: {pos}={map[pos.x][pos.y]} + {movement} == {next}={map[next.x][next.y]}"
            )
    return moved


def can_move(map, pos, movement):
    next = next_pos(pos, movement)

    match map[next.x][next.y]:
        case Tile.SPACE.value:
            return True
        case Tile.WALL.value:
            return False
        case Tile.OBST.value:
            return can_move(map, next, movement)
        case Tile.WIDE_OBST_LEFT.value | Tile.WIDE_OBST_RIGHT.value:
            if movement in (LEFT, RIGHT):
                return can_move(map, next, movement)
            other_side = (
                LEFT if map[next.x][next.y] == Tile.WIDE_OBST_RIGHT.value else RIGHT
            )
            return can_move(map, next, movement) and can_move(
                map, next_pos(next, other_side), movement
            )
        case _:
            raise ValueError("Invalid movement")


def do_move(map, pos, movement):
    next = next_pos(pos, movement)

    match map[next.x][next.y]:
        case Tile.SPACE.value:
            map[next.x][next.y] = map[pos.x][pos.y]
            map[pos.x][pos.y] = Tile.SPACE.value
        case Tile.OBST.value:
            do_move(map, next, movement)
            do_move(map, pos, movement)
        case Tile.WIDE_OBST_LEFT.value | Tile.WIDE_OBST_RIGHT.value:
            if movement in (LEFT, RIGHT):
                do_move(map, next, movement)
                do_move(map, pos, movement)
            else:
                other_side = (
                    LEFT if map[next.x][next.y] == Tile.WIDE_OBST_RIGHT.value else RIGHT
                )
                do_move(map, next, movement)
                do_move(map, next_pos(next, other_side), movement)
                do_move(map, pos, movement)
        case _:
            raise ValueError("Invalid movement")
    return next


def next_pos(position, movement):
    return Vector(position.x + movement.x, position.y + movement.y)


def calc_coords(map):
    for i, row in enumerate(map):
        for j, col in enumerate(row):
            if col in (Tile.OBST.value, Tile.WIDE_OBST_LEFT.value):
                yield 100 * i + j


def find_robot(map):
    for i, row in enumerate(map):
        for j, col in enumerate(row):
            if col == Tile.ROBOT.value:
                return Vector(i, j)
    raise ValueError("cannot find robot")


def show(map):
    for line in map:
        for ch in line:
            if ch == Tile.ROBOT.value:
                print(boldred(ch), end="")
            else:
                print(ch, end="")
        print()


def boldred(s):
    start = "\033[1;31m"
    end = "\033[0;0m"
    return f"{start}{s}{end}"


def wide_map(map):
    wide = [[Tile.SPACE.value] * len(map[0]) * 2 for _ in map]
    for i, row in enumerate(map):
        for j in range(0, len(map[i])):
            match map[i][j]:
                case Tile.OBST.value:
                    wide[i][j * 2] = Tile.WIDE_OBST_LEFT.value
                    wide[i][j * 2 + 1] = Tile.WIDE_OBST_RIGHT.value
                case Tile.WALL.value:
                    wide[i][j * 2] = Tile.WALL.value
                    wide[i][j * 2 + 1] = Tile.WALL.value
                case Tile.ROBOT.value:
                    wide[i][j * 2] = Tile.ROBOT.value
    return wide


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

    print(f"Part 1: {total_coords(deepcopy(map), movements)}")
    print(f"Part 2: {total_coords(wide_map(deepcopy(map)), movements)}")


if __name__ == "__main__":
    main()
