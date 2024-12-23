from collections import namedtuple, defaultdict
from functools import reduce
import re
import sys

Vector = namedtuple("Vector", "x y".split())

RE_INPUT = re.compile(r"^p=(\d+),(\d+) v=(-?\d+),(-?\d+)$")


def safety(robots, width, height):
    map = after_seconds(robots, width, height)
    show(map, width, height)

    quadrants = per_quadrant(map, width, height)
    return reduce((lambda a, b: a * b), quadrants)


def after_seconds(robots, width, height, n_seconds=100):
    positions = []
    for pos, movement in robots:
        positions.append(
            Vector(
                ((movement.x * n_seconds) + pos.x) % width,
                ((movement.y * n_seconds) + pos.y) % height,
            )
        )
    return positions


def per_quadrant(positions, width, height):
    # Width and height are guaranteed to be odd numbers
    quadrants = [0] * 4
    for pos in positions:
        if pos.x < width // 2:
            if pos.y < height // 2:
                quadrants[0] += 1
            elif pos.y > height // 2:
                quadrants[2] += 1
        elif pos.x > width // 2:
            if pos.y < height // 2:
                quadrants[1] += 1
            elif pos.y > height // 2:
                quadrants[3] += 1
    return quadrants


def show(positions, width, height):
    occupied = defaultdict(int)
    for pos in positions:
        occupied[pos] += 1

    for y in range(height):
        for x in range(width):
            if occupied[(x, y)]:
                print(occupied[(x, y)], end="")
            else:
                print(".", end="")
        print()


def read_robots(f):
    robots = []
    for line in f.readlines():
        m = RE_INPUT.match(line.strip())
        robots.append(
            (
                Vector(int(m.group(1)), int(m.group(2))),
                Vector(int(m.group(3)), int(m.group(4))),
            )
        )
    return robots


def main():
    infile = sys.argv[1]
    width = int(sys.argv[2])
    height = int(sys.argv[3])

    with open(infile) as f:
        robots = read_robots(f)

    print(f"Part 1: {safety(robots, width, height)}")


if __name__ == "__main__":
    main()
