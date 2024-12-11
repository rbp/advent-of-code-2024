from copy import deepcopy
import sys


def after_blinks(stones, n_blinks):
    for blink in range(n_blinks):
        stone = stones[0]
        prev = None
        while stone is not None:
            new, split = apply_rules(stone)
            if prev is None:
                stones[0] = new
            else:
                prev[1] = new

            if not split:
                stone = new[1]
                prev = new
            else:
                stones[1] += 1
                stone = new[1][1]
                prev = new[1]
    return stones[1]


def apply_rules(stone):
    if stone[0] == "0":
        return ["1", stone[1]], False

    if len(stone[0]) % 2 == 0:
        mid = len(stone[0]) // 2
        first = stone[0][:mid].lstrip("0")
        second = stone[0][mid:]
        second = f'{second[:-1].lstrip("0")}{second[-1]}'
        return [first, [second, stone[1]]], True

    return [str(int(stone[0]) * 2024), stone[1]], False


def stone_line(stone_list):
    prev = None
    for stone in stone_list[::-1]:
        prev = [stone, prev]
    return [prev, len(stone_list)]


def main():
    infile = sys.argv[1]
    with open(infile) as f:
        stones = stone_line(f.read().split())
    print(f"Part 1: {after_blinks(stones, 25)}")


if __name__ == "__main__":
    main()
