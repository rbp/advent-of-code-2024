from collections import namedtuple
import re
import sys

Point = namedtuple("Point", "x y".split())

RE_BUTTON_COORDS = re.compile(r"^Button [AB]: X\+(\d+), Y\+(\d+)$")
RE_PRIZE_COORDS = re.compile(r"^Prize: X=(\d+), Y=(\d+)$")

ADDED = 10000000000000


def total_tokens(machines):
    return sum(tokens(machine) for machine in machines)


def tokens(machine):
    tokens = {
        "a": 3,
        "b": 1,
    }
    a, b, prize = machine
    mul_b = (a.y * prize.x - prize.y * a.x) / (a.y * b.x - b.y * a.x)
    if mul_b != int(mul_b):
        return 0
    mul_b = int(mul_b)

    mul_a = (prize.x - (mul_b * b.x)) / a.x
    if mul_a != int(mul_a):
        return 0
    mul_a = int(mul_a)

    return tokens["a"] * mul_a + tokens["b"] * int(mul_b)


def mul(point, multiplier):
    return Point(point.x * multiplier, point.y * multiplier)


def read_machines(f):
    # Each machine a tuple of 3 Points:
    # (buttonA, buttonB, prize)
    machines = []

    lines = [l for l in f.read().splitlines() if l]
    i = 0
    while i < len(lines):
        re_button_a = RE_BUTTON_COORDS.match(lines[i])
        re_button_b = RE_BUTTON_COORDS.match(lines[i + 1])
        re_prize = RE_PRIZE_COORDS.match(lines[i + 2])

        machines.append(
            tuple(
                Point(int(m.group(1)), int(m.group(2)))
                for m in (re_button_a, re_button_b, re_prize)
            )
        )
        i += 3
    return machines


def corrected_machines(machines):
    return [(a, b, Point(prize.x + ADDED, prize.y + ADDED)) for a, b, prize in machines]


def main():
    infile = sys.argv[1]
    with open(infile) as f:
        machines = read_machines(f)

    print(f"Part 1: {total_tokens(machines)}")
    print(f"Part 2: {total_tokens(corrected_machines(machines))}")


if __name__ == "__main__":
    main()
