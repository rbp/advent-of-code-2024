from collections import defaultdict
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


def most_bananas(seeds, n=2000):
    prices_per_change = defaultdict(list)
    for seed in seeds:
        number = seed
        changes = {}
        last_four = [(number % 10, None)]
        for i in range(n):
            number = next_n(number)
            this_price = number % 10
            this_change = (number % 10) - last_four[-1][0]
            last_four.append((this_price, this_change))
            if len(last_four) < 4:
                continue

            if last_four[0][1] is not None:
                change = tuple([i[1] for i in last_four])
                price = last_four[-1][0]
                if change not in changes:
                    # The bloody monkey only looks at the first time a specific change happens...
                    changes[change] = price
            last_four = last_four[1:]

        # Merge this seed's changes with the main count
        for change, price in changes.items():
            prices_per_change[change].append(price)

    max_bananas = max([sum(prices) for prices in prices_per_change.values()])
    return max_bananas


def max_bananas_for(price, seeds, changes):
    all_changes = [
        changeset for seed in seeds for changeset in changes[seed].get(price, [])
    ]

    return price * max(
        sum([changeset in changes[seed][price] for seed in seeds])
        for changeset in all_changes
    )


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
    print(f"Part 2: {most_bananas(seeds)}")


if __name__ == "__main__":
    main()
