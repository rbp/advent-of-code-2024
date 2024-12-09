import sys


def defrag_checksum(disk):
    map = expand(disk)
    defrag(map)
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

    return cs


def main():
    infile = sys.argv[1]
    with open(infile) as f:
        disk = [int(i) for i in f.read().strip()]
    print(f"Part 1: {defrag_checksum(disk)}")


if __name__ == "__main__":
    main()
