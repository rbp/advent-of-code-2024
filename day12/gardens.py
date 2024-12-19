from collections import namedtuple
from dataclasses import dataclass
import sys

Pos = namedtuple("Pos", "x y".split())


@dataclass
class Region:
    id: int
    letter: str
    starting_position: Pos
    area: int
    perimeter: int
    sides: int = 0


def traverse(farm):
    regions = []
    i = 0
    while i < len(farm):
        j = 0
        while j < len(farm[i]):
            if not visited(farm, Pos(i, j)):
                regions.append(map_region(farm, Pos(i, j), len(regions)))
            j += 1
        i += 1

    return regions


def price(farm, regions, bulk=False):
    if not bulk:
        return sum(region.area * region.perimeter for region in regions)

    calculate_sides(farm, regions)
    return sum(region.area * region.sides for region in regions)


def calculate_sides(farm, regions):
    # Sweep the farm in all directions and count sides
    # i.e., for each column, if there's a change in region *and* the region of the plot is different to the one
    #   on its left, it's a new side
    # (Yes, it's inefficient, but good enough and simpler than doing a single or even 2 passes)
    region_lookup = {region.id: region for region in regions}

    calculate_horizontal_sides(
        farm, region_lookup, row_ids=range(len(farm)), lookback=1
    )
    calculate_horizontal_sides(
        farm, region_lookup, row_ids=range(len(farm) - 1, -1, -1), lookback=-1
    )

    calculate_vertical_sides(
        farm, region_lookup, col_ids=range(len(farm[0])), lookback=1
    )
    calculate_vertical_sides(
        farm, region_lookup, col_ids=range(len(farm[0]) - 1, -1, -1), lookback=-1
    )


def calculate_horizontal_sides(farm, region_lookup, row_ids, lookback):
    # region_by_id = {region.id: region for region in regions}
    first_row = row_ids[0]

    for row in row_ids:
        prev = None
        prev_part_of_side = True
        for col in range(len(farm[row])):
            plot = farm[row][col]
            if row == first_row or farm[row - lookback][col] != plot:
                if plot != prev or not prev_part_of_side:
                    region_lookup[plot].sides += 1
                prev_part_of_side = True
            else:
                prev_part_of_side = False
            prev = plot


def calculate_vertical_sides(farm, region_lookup, col_ids, lookback):
    # This assumes, for simplicity, that all rows have the same length.
    first_col = col_ids[0]

    for col in col_ids:
        prev = None
        prev_part_of_side = True
        for row in range(len(farm)):
            plot = farm[row][col]
            if col == first_col or farm[row][col - lookback] != plot:
                if plot != prev or not prev_part_of_side:
                    region_lookup[plot].sides += 1
                prev_part_of_side = True
            else:
                prev_part_of_side = False
            prev = plot


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

    return Region(region_id, letter, starting_position, area, perimeter)


def visited(farm, pos):
    return isinstance(farm[pos.x][pos.y], int)


def in_farm(farm, pos):
    return 0 <= pos.x < len(farm) and 0 <= pos.y < len(farm[pos.x])


def in_region(farm, pos, region_id):
    return pos and in_farm(farm, pos) and farm[pos.x][pos.y] == region_id


def move(farm, pos, delta):
    next = Pos(pos.x + delta.x, pos.y + delta.y)
    return next if in_farm(farm, next) else None


def initial_direction(farm, pos, region_id):
    directions = right, down, left, up = Pos(0, 1), Pos(1, 0), Pos(0, -1), Pos(-1, 0)
    for d in directions:
        if in_region(farm, move(farm, pos, d), region_id):
            return d


def next_pos(farm, pos, direction, region_id, plot_visited):
    directions = left, down, right, up = Pos(0, -1), Pos(1, 0), Pos(0, 1), Pos(-1, 0)
    turns = {
        right: [up, down, left],
        down: [right, left, up],
        left: [down, up, right],
        up: [left, right, down],
    }
    attempts = [
        (turns[direction][0], 1),
        (direction, 0),
        (turns[direction][1], 1),
        # U-turn
        (turns[direction][2], 2),
    ]

    for next_direction, incr in attempts:
        attempted_move = move(farm, pos, next_direction)
        if attempted_move is None or not in_region(farm, attempted_move, region_id):
            continue

        next = attempted_move
        for d in directions:
            plot = move(farm, next, d)
            if plot == pos or plot not in plot_visited:
                continue
            if not in_region(farm, plot, region_id):
                incr -= 2

        return next, next_direction, incr
    else:
        # Cannot move. Single plot
        return pos, None, 0


def neighbours(farm, pos, region_id):
    directions = Pos(0, -1), Pos(1, 0), Pos(0, 1), Pos(-1, 0)
    return len(
        [d for d in directions if in_region(farm, move(farm, pos, d), region_id)]
    )


def read_map(f):
    return [list(line.strip()) for line in f.readlines()]


def main():
    infile = sys.argv[1]
    with open(infile) as f:
        farm = read_map(f)
    regions = traverse(farm)
    print(f"Part 1: {price(farm, regions)}")
    print(f"Part 2: {price(farm, regions, bulk=True)}")


if __name__ == "__main__":
    main()
