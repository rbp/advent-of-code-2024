import sys


def n_safe_reports(reports, dampen=False):
    return len([r for r in reports if is_safe(r, dampen=dampen)])

def is_right_direction(report, increasing, idx):
    if increasing:
        return report[idx+1] > report[idx]
    return report[idx+1] < report[idx]

def is_step_safe(report, increasing, idx):
    return is_right_direction(report, increasing, idx) and \
            1 <= abs(report[idx+1] - report[idx]) <= 3

def is_safe(report, i=0, dampen=False):
    increasing = report[1] > report[0]
    while i < len(report) - 1:
        if is_step_safe(report, increasing, i):
            i += 1
            continue
        if not dampen:
            return False
        # If (i, i+1) is unsafe, we try to remove i, then i+1
        if is_safe(report[:i] + report[i+1:], max(i-1, 0)):
            return True
        # Ugly special case, but the very first element can force a change in direction...
        if i == 1:
            if is_safe(report[i:], 0):
                return True    
        return is_safe(report[:i+1] + report[i+2:], i)
    return True


def read_reports(f):
    return [[int(i) for i in line.split()]
            for line in f]


def main():
    infile = sys.argv[1]
    with open(infile) as f:
        reports = read_reports(f)
    print(f"Part 1: {n_safe_reports(reports)}")
    print(f"Part 2: {n_safe_reports(reports, dampen=True)}")


if __name__ == '__main__':
    main()

# Part 1: 332
# Part 2: 398