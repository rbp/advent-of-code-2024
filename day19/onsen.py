from functools import lru_cache
from collections import defaultdict
import sys


def possible_designs(patterns, towels):
    patlookup = mklookup(patterns)

    possible = 0
    for towel in towels:
        if is_design_possible(towel, patlookup):
            possible += 1
    return possible


def is_design_possible(towel, lookup, possible_until=0):
    if possible_until == len(towel):
        return True

    for pattern in lookup[towel[possible_until]]:
        if towel[possible_until : possible_until + len(pattern)] != pattern:
            continue
        possible = is_design_possible(towel, lookup, possible_until + len(pattern))
        if possible:
            return True

    return False


PATLOOKUP = None


def all_possible_patterns(patterns, towels):
    global PATLOOKUP
    PATLOOKUP = mklookup(patterns)

    designs = 0
    for towel in towels:
        designs += n_possible_arrangements(towel)
    return designs


# def n_possible_arrangements(towel, lookup):
#     designs = 0
#     subdesigns = [towel]
#     while subdesigns:
#         d = subdesigns.pop()
#         patterns = [p for p in lookup[d[0]] if d[: len(p)] == p]
#         remaining = [d[len(p) :] for p in patterns]
#         designs += len([d for d in remaining if len(d) == 0])
#         subdesigns.extend([d for d in remaining if len(d) > 0])

#     return designs


@lru_cache
def n_possible_arrangements(design):
    if not design:
        return 1

    designs = 0
    for pattern in PATLOOKUP[design[0]]:
        if design[: len(pattern)] != pattern:
            continue
        designs += n_possible_arrangements(design[len(pattern) :])

    return designs


def mklookup(patterns):
    lookup = defaultdict(list)
    for p in patterns:
        lookup[p[0]].append(p)

    for pl in lookup.values():
        pl.sort(key=lambda p: len(p))
    return lookup


def read_input(f):
    patterns = [p for p in f.readline().strip().split(", ")]
    f.readline()
    towels = f.read().splitlines()
    return patterns, towels


def main():
    infile = sys.argv[1]
    with open(infile) as f:
        patterns, towels = read_input(f)

    print(f"Part 1: {possible_designs(patterns, towels)}")
    print(f"Part 2: {all_possible_patterns(patterns, towels)}")


if __name__ == "__main__":
    main()
