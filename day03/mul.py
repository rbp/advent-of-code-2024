import sys
import re


RE_MUL = re.compile(r'mul\(([0-9]+),([0-9]+)\)')
RE_DO = re.compile(r"do\(\)")
RE_DONT = re.compile(r"don't\(\)")


def mul(memory):
    return sum(int(a)*int(b) for a, b in RE_MUL.findall(memory))

def enabled_mul(memory):
    s = 0
    i = 0
    while i < len(memory):
        dont = RE_DONT.search(memory, i)
        if dont is not None:
            start = dont.start()
            end = dont.end()
        else:
            start = end = len(memory)
        s += sum(int(a)*int(b) for a, b in RE_MUL.findall(memory, i, start))

        do = RE_DO.search(memory, end)
        if do is not None:
            i = do.end()
        else:
            i = len(memory)
    return s

def main():
    infile = sys.argv[1]
    with open(infile) as f:
        memory = f.read().strip()
    print(f"Part 1: {mul(memory)}")
    print(f"Part 2: {enabled_mul(memory)}")


if __name__ == '__main__':
    main()
