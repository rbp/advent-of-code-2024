import sys


def sum_valid(equations, concat=False):
    return sum(
        result for result, digits in equations if valid(result, digits, concat=concat)
    )


def valid(result, digits, concat=False, so_far=0):
    if not digits:
        return so_far == result

    return (
        valid(result, digits[1:], concat=concat, so_far=so_far + digits[0])
        or valid(result, digits[1:], concat=concat, so_far=so_far * digits[0])
        or (
            concat
            and valid(
                result, digits[1:], concat=concat, so_far=int(f"{so_far}{digits[0]}")
            )
        )
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
    print(f"Part 2: {sum_valid(eqs, concat=True)}")


if __name__ == "__main__":
    main()
