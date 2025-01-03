from functools import lru_cache
import sys


def nth_number(seeds, n=2000):
    summed = 0
    for seed in seeds:
        number = seed
        for i in range(n):
            number = next_n(number)
        summed += number
    return summed


@lru_cache(maxsize=1024 * 1024)
def next_n(number):
    r = number * 64
    r = mix(r, number)
    number = prune(r)

    r = number // 32
    r = mix(r, number)
    number = prune(r)

    r = number * 2048
    r = mix(r, number)
    number = prune(r)
    return number


@lru_cache(maxsize=1024 * 1024)
def mix(a, b):
    return a ^ b


@lru_cache(maxsize=1024 * 1024)
def prune(a):
    return a % 16777216


def read_seeds(f):
    return [int(i) for i in f.read().splitlines()]


def main():
    infile = sys.argv[1]
    with open(infile) as f:
        seeds = read_seeds(f)

    print(f"Part 1: {nth_number(seeds)}")


if __name__ == "__main__":
    main()
