import sys


def n_safe_reports(reports):
    return len([r for r in reports if is_safe(r)])

def right_direction(report, increasing, idx):
    if increasing:
        return report[idx] > report[idx-1]
    return report[idx] < report[idx-1]

def unsafe(report, increasing, idx):
    return not(
        right_direction(report, increasing, idx) and
            1 <= abs(report[idx] - report[idx-1]) <= 3
    )

def is_safe(report):
    increasing = report[1] > report[0]
    for i in range(1, len(report)):
        if unsafe(report, increasing, i):
            return False
    return True

def read_reports(f):
    return [[int(i) for i in line.split()]
            for line in f]


def main():
    infile = sys.argv[1]
    with open(infile) as f:
        reports = read_reports(f)
    print(f"Part 1: {n_safe_reports(reports)}")


if __name__ == '__main__':
    main()