from collections import defaultdict
import sys


def count_antinodes(map):
    # For every pair of antennae of the same type ("frequency"), get the delta (i, j) between them.
    # There's one antinode this delta away from one antenna, and one in the other direction
    # from the other.
    # antinodes outside the map don't count.
    # Storing the antinode coordinates as (i, j) pairs in a set, you get the total unique count.
    antennae = defaultdict(list)
    for i in range(len(map)):
        for j in range(len(map[i])):
            if is_antenna(map[i][j]):
                antennae[map[i][j]].append((i, j))

    unique_antinodes = set()
    for freq in antennae:
        towers = antennae[freq]
        for i in range(len(towers) - 1):
            for j in range(i + 1, len(towers)):
                a1, a2 = towers[i], towers[j]
                delta = (a2[0] - a1[0], a2[1] - a1[1])
                antinodes = (
                    (a1[0] - delta[0], a1[1] - delta[1]),
                    (a2[0] + delta[0], a2[1] + delta[1]),
                )
                for antinode in antinodes:
                    if inside(map, antinode):
                        unique_antinodes.add(antinode)
    return len(unique_antinodes)


def is_antenna(ch: str):
    return ch.isalnum()


def inside(map, point):
    return 0 <= point[0] < len(map) and 0 <= point[1] < len(map[point[0]])


def read_map(f):
    return [list(line.strip()) for line in f.readlines()]


def main():
    infile = sys.argv[1]
    with open(infile) as f:
        map = read_map(f)
    print(f"Part 1: {count_antinodes(map)}")


if __name__ == "__main__":
    main()
