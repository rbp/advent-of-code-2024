import sys

def xmas(puzzle):
    found = 0
    for i, line in enumerate(puzzle):
        for j, ch in enumerate(line):
            if ch != 'X':
                continue
            for next in directions.values():
                if find(puzzle, next(i, j), 'MAS', next):
                    found += 1
    return found

def x_mas(puzzle):
    remaining = {
        'M': 'AS',
        'S': 'AM'
    }
    found = 0
    for i, line in enumerate(puzzle):
        for j, ch in enumerate(line):
            if ch not in 'MS':
                continue
            down_right = directions["diag_down_right"]
            down_left = directions["diag_down_left"]
            if find(puzzle, down_right(i, j), remaining[ch], down_right) and \
                (
                    find(puzzle, (i, j+2), 'MAS', down_left) or
                    find(puzzle, (i, j+2), 'SAM', down_left)
                ):
                found += 1
    return found


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
    print(f"Part 2: {x_mas(puzzle)}")

if __name__ == '__main__':
    main()