import sys


class GuardUp:
    def next(self, i, j):
        return i - 1, j

    def turn(self):
        return Guard(">")


class GuardRight:
    def next(self, i, j):
        return i, j + 1

    def turn(self):
        return Guard("v")


class GuardDown:
    def next(self, i, j):
        return i + 1, j

    def turn(self):
        return Guard("<")


class GuardLeft:
    def next(self, i, j):
        return i, j - 1

    def turn(self):
        return Guard("^")


def Guard(ch):
    match ch:
        case "^":
            return GuardUp()
        case ">":
            return GuardRight()
        case "v":
            return GuardDown()
        case "<":
            return GuardLeft()
        case _:
            raise ValueError


WALL = "#"


def positions(map):
    guard, i, j = find_guard(map)
    map[i][j] = "."
    n_pos = 0
    while not outside(map, i, j):
        while wall_at(map, *guard.next(i, j)):
            guard = guard.turn()
        if not visited(map, i, j):
            map[i][j] = "X"
            n_pos += 1
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
    return not outside(map, i, j) and map[i][j] == WALL


def outside(map, i, j):
    return not (0 <= i < len(map) and 0 <= j < len(map[i]))


def visited(map, i, j):
    return map[i][j] == "X"


def read_map(f):
    return [list(line) for line in f.readlines()]


def main():
    infile = sys.argv[1]
    with open(infile) as f:
        map = read_map(f)
    print(f"Part 1: {positions(map)}")


if __name__ == "__main__":
    main()
