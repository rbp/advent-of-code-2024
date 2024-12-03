import sys
import re


def mul(memory):
    re_mul = r'mul\(([0-9]+),([0-9]+)\)'
    return sum(int(a)*int(b) for a, b in re.findall(re_mul, memory))


def main():
    infile = sys.argv[1]
    with open(infile) as f:
        memory = f.read().strip()
    print(f"Part 1: {mul(memory)}")


if __name__ == '__main__':
    main()
