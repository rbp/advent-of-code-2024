from copy import deepcopy
import sys


class LoopException(Exception):
    pass


class GuardUp:
    ch = "^"

    def next(self, i, j):
        return i - 1, j

    def turn(self):
        return Guard(">")


class GuardRight:
    ch = ">"

    def next(self, i, j):
        return i, j + 1

    def turn(self):
        return Guard("v")


class GuardDown:
    ch = "v"

    def next(self, i, j):
        return i + 1, j

    def turn(self):
        return Guard("<")


class GuardLeft:
    ch = "<"

    def next(self, i, j):
        return i, j - 1

    def turn(self):
        return Guard("^")


ALL_GUARDS = [GuardUp, GuardRight, GuardDown, GuardLeft]


def Guard(ch):
    for guard in ALL_GUARDS:
        if ch == guard.ch:
            return guard()
    raise ValueError


def positions(map):
    return traverse(map, find_guard(map))


def loops(map):
    fresh_map = deepcopy(map)
    starting = find_guard(map)
    obstacles = set()

    def try_obstacle(guard, i, j):
        nonlocal starting, obstacles, fresh_map
        if (i, j) != starting[1:] and (i, j) not in obstacles:
            new_map = deepcopy(fresh_map)
            new_map[i][j] = "#"
            try:
                traverse(new_map, starting)
            except LoopException:
                obstacles.add((i, j))

    traverse(map, starting, at_step=try_obstacle)

    return len(obstacles)


def traverse(map, starting, at_step=lambda guard, i, j: None):
    guard, i, j = starting

    n_pos = 1
    while not outside(map, i, j):
        while wall_at(map, *guard.next(i, j)):
            guard = guard.turn()

        at_step(guard, i, j)

        if (i, j) != starting[1:] and map[i][j] == guard.ch:
            raise LoopException

        if not visited(map, i, j):
            n_pos += 1
        map[i][j] = guard.ch
        i, j = guard.next(i, j)
    return n_pos


def find_guard(map):
    for i, line in enumerate(map):
        for j, ch in enumerate(line):
            try:
                guard = Guard(map[i][j])
                return guard, i, j
            except ValueError:
                pass


def wall_at(map, i, j):
    return not outside(map, i, j) and map[i][j] == "#"


def outside(map, i, j):
    return not (0 <= i < len(map) and 0 <= j < len(map[i]))


def visited(map, i, j):
    return map[i][j] in [g.ch for g in ALL_GUARDS]


def read_map(f):
    return [list(line) for line in f.readlines()]


def main():
    infile = sys.argv[1]
    with open(infile) as f:
        map = read_map(f)
    print(f"Part 1: {positions(deepcopy(map))}")
    print(f"Part 2: {loops(deepcopy(map))}")


if __name__ == "__main__":
    main()
