import sys

def xmas(puzzle):
    found_at = []
    for i, line in enumerate(puzzle):
        for j, ch in enumerate(line):
            if ch != 'X':
                continue
            # breakpoint()
            for direction in [
                "up",
                "diag_up_right",
                "right",
                "diag_down_right",
                "down",
                "diag_down_left",
                "left",
                "diag_up_left"]:
                if find(puzzle, direction, next(direction, i, j), 'MAS'):
                    found_at.append((i, j))
    return len(found_at)

def next(direction, i, j):
    match direction:
        case "up":
            return i-1, j
        case "diag_up_right":
            return i-1, j+1
        case "right":
            return i, j+1
        case "diag_down_right":
            return i+1, j+1
        case "down":
            return i+1, j
        case "diag_down_left":
            return i+1, j-1
        case "left":
            return i, j-1
        case "diag_up_left":
            return i-1, j-1
        case _:
            raise ValueError

def find(puzzle, direction, at, word_left):
    if not word_left:
        return True
    i, j = at[0], at[1]
    # FIXME: short-circuit when there's no space left to search
    if not(
        0 <= i < len(puzzle) and 0 <= j < len(puzzle[i])):
        return False
    if puzzle[i][j] != word_left[0]:
        return False
    return find(puzzle, direction, next(direction, i, j), word_left[1:])


def read_puzzle(f):
    return f.readlines()

def main():
    infile = sys.argv[1]
    with open(infile) as f:
        puzzle = read_puzzle(f)
    print(f"Part 1: {xmas(puzzle)}")

if __name__ == '__main__':
    main()