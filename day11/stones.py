from collections import namedtuple
from functools import cache
import sys


Stone = namedtuple("Stone", "number qty".split())


def after_blinks(stones, n_blinks):
    return sum(sum(s.qty for s in blink_n_times(stone, n_blinks)) for stone in stones)


def blink_n_times(original_stone, n_blinks):
    """
    Blink original_stone
    returns a compact representation. For instance,
    [('0', 3), ('4', 4), ('6', 1), ('8', 3), ('9', 1), ('20', 1), ('24', 1)]
    """
    current_gen = [original_stone]

    blinks = 0
    while blinks < n_blinks:

        # Blink the remaining times
        next_gen = []
        for stone in current_gen:
            it = apply_rules(stone)
            next_gen = merge(next_gen, it)
        current_gen = next_gen
        blinks += 1
    return current_gen


@cache
def apply_rules(stone):
    num, qty = stone
    if num == "0":
        return (Stone("1", qty),)

    if len(num) % 2 == 0:
        mid = len(num) // 2
        first = Stone(num[:mid].lstrip("0"), qty)
        second = Stone(num[mid:].lstrip("0") or "0", qty)
        return merge([first], [second])

    return (Stone(str(int(num) * 2024), qty),)


def compact(stones):
    """Return a compact representation of a list of stone values
    For instance, '0' after 7 blinks is
    ['4', '0', '4', '8', '20', '24', '4', '0', '4', '8', '8', '0', '9', '6']
    Sorted, is
    ['0', '0', '0', '4', '4', '4', '4', '6', '8', '8', '8', '9', '20', '24']
    The compact representation is
    [('0', 3), ('4', 4), ('6', 1), ('8', 3), ('9', 1), ('20', 1), ('24', 1)]
    """
    repr = []
    i = 0
    stones = sorted(stones, key=lambda s: int(i))
    while i < len(stones):
        el = stones[i]
        j = i + 1
        while j < len(stones) and stones[i] == stones[j]:
            j += 1
        repr.append(Stone(el, j - i))
        i = j
    return tuple(repr)


def merge(c1, c2):
    """
    Merge 2 compact representations. e.g.,
    merge(
        [('0', 1), ('4', 1), ('6', 1), ('8', 3)],
        [('0', 2), ('4', 3), ('9', 1), ('20', 1), ('24', 1)]]
    ) == [
        ('0', 3), ('4', 4), ('6', 1), ('8', 3), ('9', 1), ('20', 1), ('24', 1)
    ]
    """
    i = j = 0
    new = []
    while i < len(c1) and j < len(c2):
        if c1[i].number < c2[j].number:
            new.append(c1[i])
            i += 1
        elif c2[j].number < c1[i].number:
            new.append(c2[j])
            j += 1
        elif c1[i].number == c2[j].number:
            new.append(Stone(number=c1[i].number, qty=c1[i].qty + c2[j].qty))
            i += 1
            j += 1
    if i < len(c1):
        new.extend(c1[i:])
    if j < len(c2):
        new.extend(c2[j:])
    return tuple(new)


def main():
    infile = sys.argv[1]
    with open(infile) as f:
        stone_list = compact(f.read().split())

    print(f"Part 1: {after_blinks(stone_list, 25)}")
    print(f"Part 2: {after_blinks(stone_list, 75)}")


if __name__ == "__main__":
    main()
