from functools import reduce
import sys

def trail_scores(map):
    score = 0
    for i in range(len(map)):
        for j in range(len(map[i])):
            if map[i][j] == "0":
                endpoints = traverse_trails(map, i, j)
                score += len(set(endpoints))
    return score

def trail_ratings(map):
    rating = 0
    for i in range(len(map)):
        for j in range(len(map[i])):
            if map[i][j] == "0":
                endpoints = traverse_trails(map, i, j)
                rating += len(endpoints)

    return rating

def traverse_trails(map, i, j):
    current = map[i][j]
    if current == "9":
        return [(i, j)]
    
    return reduce(
        lambda l1, l2: l1 + l2,
        [traverse_trails(map, next_i, next_j)
            for next_i, next_j in neighbours(map, str(int(current)+1), i, j)
        ],
        [])
     
    
def neighbours(map, value, i, j):
    return [
        (next_i, next_j)
        for next_i, next_j in [
            (i-1, j),
            (i, j+1),
            (i+1, j),
            (i, j-1),
        ]
        if 0 <= next_i < len(map) and 0 <= next_j < len(map[next_i])
          and map[next_i][next_j] == value
    ]


def read_map(f):
    return [list(line.strip()) for line in f.readlines()]


def main():
    infile = sys.argv[1]
    with open(infile) as f:
        map = read_map(f)
    print(f"Part 1: {trail_scores(map)}")
    print(f"Part 2: {trail_ratings(map)}")


if __name__ == "__main__":
    main()
