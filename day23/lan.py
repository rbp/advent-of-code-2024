from collections import defaultdict
import sys


def t_lan_party(pairs):
    groups = mkgroups(pairs)
    t_triplets = mktriplets(groups, "t")

    print(t_triplets)
    return len(t_triplets)


def mkgroups(pairs):
    groups = defaultdict(set)
    for c1, c2 in pairs:
        groups[c1].add(c2)
        groups[c2].add(c1)
    return groups


def mktriplets(groups, startswith):
    t_triplets = set()
    for c, conns in groups.items():
        if not c.startswith(startswith):
            continue
        for conn in conns:
            for third in groups[conn]:
                if c in groups[third]:
                    t_triplets.add(tuple(sorted((c, conn, third))))
    return t_triplets


def read_pairs(f):
    return [line.strip().split("-") for line in f.readlines()]


def main():
    infile = sys.argv[1]
    with open(infile) as f:
        pairs = read_pairs(f)

    print(f"Part 1: {t_lan_party(pairs)}")


if __name__ == "__main__":
    main()
