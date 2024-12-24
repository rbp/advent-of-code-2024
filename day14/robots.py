from collections import namedtuple, defaultdict
from functools import reduce
import re
import sys
from time import sleep

Vector = namedtuple("Vector", "x y".split())

RE_INPUT = re.compile(r"^p=(\d+),(\d+) v=(-?\d+),(-?\d+)$")


def safety(robots, width, height):
    map = after_seconds(robots, width, height)
    show(map, width, height)

    quadrants = per_quadrant(map, width, height)
    return reduce((lambda a, b: a * b), quadrants)


def after_seconds(robots, width, height, n_seconds=100):
    positions = defaultdict(list)
    for pos, movement in robots:
        pos = Vector(
            ((movement.x * n_seconds) + pos.x) % width,
            ((movement.y * n_seconds) + pos.y) % height,
        )
        positions[pos].append(movement)
    return positions


def per_quadrant(positions, width, height):
    # Width and height are guaranteed to be odd numbers
    quadrants = [0] * 4
    for pos, robots in positions.items():
        if pos.x < width // 2:
            if pos.y < height // 2:
                quadrants[0] += len(robots)
            elif pos.y > height // 2:
                quadrants[2] += len(robots)
        elif pos.x > width // 2:
            if pos.y < height // 2:
                quadrants[1] += len(robots)
            elif pos.y > height // 2:
                quadrants[3] += len(robots)
    return quadrants


def wait_till_tree(robots, width, height):
    # This can be manually changed to visually inspect the output and be able to resume later
    block_start = 8000
    i = block_start
    while True:
        map = after_seconds(robots, width, height, n_seconds=i)

        # Let's focos on the images with busy rows
        skip = False
        row_sums = [sum([(x, y) in map for x in range(width)]) for y in range(height)]
        if max(row_sums) < 20:
            skip = True
        if skip:
            i += 1
            continue

        show(map, width, height)
        print(i)
        sleep(0.5)

        clear()
        if i > block_start + 20:
            i += 90
            block_start = i
        else:
            i += 1


def show(map, width, height):
    for y in range(height):
        for x in range(width):
            if (x, y) in map:
                print(boldgreen(len(map[(x, y)])), end="")
            else:
                print(grey("."), end="")
        print()


def clear():
    print(chr(27) + "[2J")


def grey(s):
    start = "\033[30m"
    end = "\033[0m"
    return f"{start}{s}{end}"


def boldgreen(s):
    start = "\033[1;32m"
    end = "\033[0;0m"
    return f"{start}{s}{end}"


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
    print(f"Part 2: {wait_till_tree(robots, width, height)}")


if __name__ == "__main__":
    main()
