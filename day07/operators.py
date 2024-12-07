import sys


def sum_valid(equations):
    return sum(result for result, digits in equations if valid(result, digits))


def valid(result, digits, so_far=0):
    if not digits:
        return so_far == result

    next = digits[0]
    return valid(result, digits[1:], so_far + next) or valid(
        result, digits[1:], so_far * next
    )


def read_equations(f):
    return [
        (int(line.split(":")[0]), [int(d) for d in line.split()[1:]])
        for line in f.readlines()
    ]


def main():
    infile = sys.argv[1]
    with open(infile) as f:
        eqs = read_equations(f)
    print(f"Part 1: {sum_valid(eqs)}")


if __name__ == "__main__":
    main()
