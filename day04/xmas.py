import sys

def xmas(puzzle):
    found_at = []
    for i, line in enumerate(puzzle):
        for j, ch in enumerate(line):
            if ch != 'X':
                continue
            # breakpoint()
            for next in directions.values():
                if find(puzzle, next(i, j), 'MAS', next):
                    found_at.append((i, j))
    return len(found_at)

directions = {
    "up": lambda i, j: (i-1, j),
    "diag_up_right": lambda i, j: (i-1, j+1),
    "right": lambda i, j: (i, j+1),
    "diag_down_right": lambda i, j: (i+1, j+1),
    "down": lambda i, j: (i+1, j),
    "diag_down_left": lambda i, j: (i+1, j-1),
    "left": lambda i, j: (i, j-1),
    "diag_up_left": lambda i, j: (i-1, j-1),
}


def find(puzzle, at, word_left, next):
    if not word_left:
        return True
    i, j = at[0], at[1]
    # FIXME: short-circuit when there's no space left to search
    if not(
        0 <= i < len(puzzle) and 0 <= j < len(puzzle[i])):
        return False
    if puzzle[i][j] != word_left[0]:
        return False
    return find(puzzle, next(i, j), word_left[1:], next)


def read_puzzle(f):
    return f.readlines()

def main():
    infile = sys.argv[1]
    with open(infile) as f:
        puzzle = read_puzzle(f)
    print(f"Part 1: {xmas(puzzle)}")

if __name__ == '__main__':
    main()