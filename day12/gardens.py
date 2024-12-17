from collections import namedtuple
import sys

Pos = namedtuple("Pos", "x y".split())


def price(farm):
    regions = []
    i = 0
    while i < len(farm):
        j = 0
        while j < len(farm[i]):
            if not isinstance(farm[i][j], int):
                regions.append(map_region(farm, Pos(i, j), len(regions)))
            j += 1
        i += 1

    return sum(region[2] * region[3] for region in regions)


def map_region(farm, starting_position, region_id):
    letter = farm[starting_position.x][starting_position.y]
    area = 0
    perimeter = 0

    positions = [starting_position]
    while positions:
        pos = positions.pop()
        if visited(farm, pos):
            continue
        farm[pos.x][pos.y] = region_id

        area += 1
        # Perimeter is 4 (all sides), minus any sides that touch
        # the same type of plan.
        # We deduct it twice because *both* plots need to have once edge removed.
        perimeter += 4 - 2 * sum(
            1
            for delta in [Pos(-1, 0), Pos(0, 1), Pos(1, 0), Pos(0, -1)]
            if in_farm(farm, Pos(pos.x + delta.x, pos.y + delta.y))
            and farm[pos.x + delta.x][pos.y + delta.y] == region_id
        )

        positions.extend(
            Pos(pos[0] + delta[0], pos[1] + delta[1])
            for delta in [(-1, 0), (0, 1), (1, 0), (0, -1)]
            if 0 <= pos[0] + delta[0] < len(farm)
            and (0 <= pos[1] + delta[1] < len(farm[pos[0] + delta[0]]))
            and farm[pos[0] + delta[0]][pos[1] + delta[1]] == letter
        )
    return letter, starting_position, area, perimeter


def visited(farm, pos):
    return isinstance(farm[pos.x][pos.y], int)


def in_farm(farm, pos):
    return 0 <= pos.x < len(farm) and 0 <= pos.y < len(farm[pos.x])


def read_map(f):
    return [list(line.strip()) for line in f.readlines()]


def main():
    infile = sys.argv[1]
    with open(infile) as f:
        farm = read_map(f)
    print(f"Part 1: {price(farm)}")


if __name__ == "__main__":
    main()
