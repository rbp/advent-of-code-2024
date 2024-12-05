from collections import defaultdict
import sys


def correct_updates(ordering, updates):
    cannot_after = defaultdict(set)
    for before, after in ordering:
        cannot_after[after].add(before)

    mid_sum = 0
    for update in updates:
        for i, page in enumerate(update):
            if set(update[i+1:]).intersection(cannot_after[page]):
                break
        else:
            mid_sum += int(update[len(update)//2])
    return mid_sum

def fix_order(ordering, updates):
    cannot_after = defaultdict(set)
    for before, after in ordering:
        cannot_after[after].add(before)
    
    mid_sum = 0
    for update in updates:
        fixed = False
        i = 0
        while i < len(update):
            page = update[i]
            j = i+1
            while j < len(update):
                if update[j] in cannot_after[page]:
                    fixed = True
                    # I could also swap update[i] and update[j]. More CompSci, and would work.
                    # Also avoids shifing the entire list.
                    update[i:i] = [update.pop(j)]
                    break
                j += 1
            else:
                i += 1
        if fixed:
            mid_sum += int(update[len(update)//2])
    return mid_sum

def read_input(f):
    rules = []
    line = f.readline().strip()
    while line != '':
        rules.append(line.split('|'))
        line = f.readline().strip()
    updates = [line.split(',') for line in f.read().splitlines()]
    return rules, updates


def main():
    infile = sys.argv[1]
    with open(infile) as f:
        ordering, updates = read_input(f)
    print(f"Part 1: {correct_updates(ordering, updates)}")
    print(f"Part 1: {fix_order(ordering, updates)}")

if __name__ == '__main__':
    main()