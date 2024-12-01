import sys


def pair_distance(l1, l2):
    l1.sort()
    l2.sort()
    return sum(abs(i - j) for i, j in zip(l1, l2))


def read_lists(f):
    l1 = []
    l2 = []
    for line in f:
        i1, i2 = line.split()
        l1.append(int(i1))
        l2.append(int(i2))
    return l1, l2


def main():
    infile = sys.argv[1]
    with open(infile) as f:
        l1, l2 = read_lists(f)
    print(f"Part 1: {pair_distance(l1, l2)}")

if __name__ == '__main__':
    main()