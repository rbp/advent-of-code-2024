from collections import namedtuple
import re
import sys

Point = namedtuple("Point", "x y".split())

RE_BUTTON_COORDS = re.compile(r"^Button [AB]: X\+(\d+), Y\+(\d+)$")
RE_PRIZE_COORDS = re.compile(r"^Prize: X=(\d+), Y=(\d+)$")


def total_tokens(machines):
    return sum(tokens(machine) for machine in machines)


def tokens(machine):
    tokens = {
        "a": 3,
        "b": 1,
    }
    a, b, prize = machine

    max_mul_b = min(
        [
            prize.x // b.x,
            prize.y // b.y,
        ]
    )
    mul_a = None

    mul_b = max_mul_b
    while mul_b >= 0:
        b_multipled = mul(b, mul_b)
        diff_x = prize.x - b_multipled.x
        diff_y = prize.y - b_multipled.y

        if diff_x % a.x == 0 and diff_y % a.y == 0 and diff_x // a.x == diff_y // a.y:
            mul_a = diff_x // a.x
            return tokens["a"] * mul_a + tokens["b"] * mul_b
        mul_b -= 1

    if mul_a is None:
        return 0
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


def main():
    infile = sys.argv[1]
    with open(infile) as f:
        machines = read_machines(f)

    print(f"Part 1: {total_tokens(machines)}")


if __name__ == "__main__":
    main()
