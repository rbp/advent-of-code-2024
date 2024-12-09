from collections import defaultdict
import sys


def defrag_checksum(disk):
    map = expand(disk)
    defrag(map)
    return checksum(map)


def nonfrag_checksum(disk):
    map = expand(disk)
    nonfrag(map)
    return checksum(map)


def expand(compact):
    # [ [[0, x], n_spaces],
    #   [[1, y], n_spaces],
    #   [[2, z], n_spaces]...]
    return [
        [
            [counter, int(compact[i])],
            compact[i + 1] if i + 1 < len(compact) else 0,
        ]
        for counter, i in enumerate(range(0, len(compact), 2))
    ]


def defrag(map):
    group_idx = 0
    while group_idx < len(map) - 1:
        group = map[group_idx]
        free_space = group[1]
        blocks = []
        while free_space and group_idx < len(map) - 1:
            last = map[-1][0]
            take_from_last = min(last[1], free_space)
            blocks.append((last[0], take_from_last))
            free_space -= take_from_last
            group[1] = free_space

            last[1] -= take_from_last
            map[-1][1] += take_from_last
            if not last[1]:
                map.pop()

        for block in blocks:
            group[0].extend(block)
        group_idx += 1


def nonfrag(map):
    for group_idx in range(len(map) - 1, 0, -1):
        groups_by_space = mk_space_lookup(map)
        # The goal is to move files to the *leftmost* suitable space.
        spaces = sorted(
            [k for k, v in groups_by_space.items() if v[0] < group_idx],
            key=lambda k: groups_by_space[k][0],
        )
        if not spaces:
            continue

        group = map[group_idx]
        space_found = find_lowest_space(spaces, group[0][1])
        if space_found is None:
            continue
        # pop(0)! Perhaps I can make the dict values be a stack, faster to pop
        space_group_idx = groups_by_space[space_found].pop(0)
        if not groups_by_space[space_found]:
            del groups_by_space[space_found]

        spacious_group = map[space_group_idx]
        spacious_group[0].extend(group[0][:2])
        spacious_group[1] -= group[0][1]

        map[group_idx - 1][1] += group[0][1]
        group[0][:2] = []


def find_lowest_space(spaces, el, i=0, j=None):
    # Warning, ordering is on leftmost fit, not closest fit!
    # This is a dumb, linear search.
    # A binary one needs to take the unusual ordering into account.
    i = 0
    while i < len(spaces) and spaces[i] < el:
        i += 1
    if i == len(spaces):
        return None
    return spaces[i]


def mk_space_lookup(map):
    groups_by_space = defaultdict(list)
    for i, group in enumerate(map):
        if group[1]:
            groups_by_space[group[1]].append(i)
    return groups_by_space


def checksum(map):
    cs = 0
    pos = 0
    for group in map:
        for i in range(0, len(group[0]), 2):
            fid = group[0][i]
            count = group[0][i + 1]
            for i in range(count):
                cs += pos * fid
                pos += 1
        for i in range(group[1]):
            pos += 1

    return cs


def main():
    infile = sys.argv[1]
    with open(infile) as f:
        disk = [int(i) for i in f.read().strip()]
    print(f"Part 1: {defrag_checksum(disk)}")
    print(f"Part 2: {nonfrag_checksum(disk)}")


if __name__ == "__main__":
    main()
