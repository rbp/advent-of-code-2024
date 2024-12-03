import sys
import re


RE_MUL = re.compile(r'mul\(([0-9]+),([0-9]+)\)')
RE_DO = re.compile(r"do\(\)")
RE_DONT = re.compile(r"don't\(\)")
RE_DONT_BLOCK = re.compile(r"don't\(\).*?(do\(\)|$)")


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

def enabled_mul2(memory):
    enabled = RE_DONT_BLOCK.sub(r"\1", memory)
    return sum(int(a)*int(b) for a, b in RE_MUL.findall(enabled))


def main():
    infile = sys.argv[1]
    with open(infile) as f:
        memory = "".join(line.strip() for line in f.readlines())    
    print(f"Part 1: {mul(memory)}")
    print(f"Part 2: {enabled_mul(memory)}")
    print(f"Part 2/b: {enabled_mul2(memory)}")


if __name__ == '__main__':
    main()
