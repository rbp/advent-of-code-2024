from copy import deepcopy
import heapq
import sys

UP = (-1, 0)
RIGHT = (0, 1)
DOWN = (1, 0)
LEFT = (0, -1)
DIRECTIONS = UP, RIGHT, DOWN, LEFT
OPPOSITE = {UP: DOWN, DOWN: UP, LEFT: RIGHT, RIGHT: LEFT}


def lowest_score(scores, start):
    return scores[start[0]][start[1]][0]


def tiles_in_best_paths(maze, scores, start, end, best_score):
    tiles = set()
    paths = best_paths(maze, start, RIGHT, end, scores, best_score)

    for path in paths:
        tiles.update(path)

    # show_paths(maze, tiles)
    return len(tiles)


def best_paths(
    maze, node, direction, end, scores, best_score, score=0, path=None, visited=None
):
    if path is None:
        path = []
    if visited is None:
        visited = set()

    if node == end:
        if score == best_score:
            return [path + [node]]
        return []

    paths = []
    for neighbour, direction_from_node in find_unvisited_neighbours(
        maze, node, visited
    ):
        if score + scores[neighbour[0]][neighbour[1]][0] > best_score + 1:
            continue

        path_score = score + 1
        if direction != direction_from_node:
            path_score += 1000
        traversed = best_paths(
            maze,
            neighbour,
            direction_from_node,
            end,
            scores,
            best_score,
            score=path_score,
            path=path + [node],
            visited=visited | {node},
        )
        for p in traversed:
            paths.append(p)

    return paths


def dijkstra(maze, start, end):
    """Direction-aware Dikstra: calculates the cost for getting to the end
    depending on which direction you're coming into a node from the previous one.
    """
    # scores[x][y] = {direction1: score1, direction2: score2...}
    # where "direction" is a possible direction to continue to
    # That is: to continue in direction1, the score is score1
    # scores = [[{}] * len(maze[0]) for _ in maze]

    # scores[x][y] = (score, direction)
    # That is, the score from (x, y) to the end, following direction
    scores = [[None] * len(maze[0]) for _ in maze]

    # At the end position, your score to get to the end is always zero,
    # regardless of where you're coming from
    # scores[end[0]][end[1]] = {d: 0 for d in DIRECTIONS}
    scores[end[0]][end[1]] = (0, None)

    # To be able to heapify it, unvisited is a list of (score, position)
    unvisited = [(0, end)]
    while unvisited:
        _, node = heapq.heappop(unvisited)

        node_score, node_direction = scores[node[0]][node[1]]

        # Set the neighbours' score, depending on where they're coming from
        for neighbour, direction_to_node in find_unscored_neighbours(
            maze, node, scores
        ):
            score = node_score + 1
            if (node_direction is not None and node_direction != direction_to_node) or (
                neighbour == start and direction_to_node != RIGHT
            ):
                score += 1000

            scores[neighbour[0]][neighbour[1]] = (score, direction_to_node)
            heapq.heappush(unvisited, (score, neighbour))

    return scores


def find_unscored_neighbours(maze, pos, scores):
    """Return (neighbour, direction_to_reach_pos)"""
    for direction in (UP, RIGHT, DOWN, LEFT):
        neighbour = (pos[0] + direction[0], pos[1] + direction[1])
        if (
            maze[neighbour[0]][neighbour[1]] != "#"
            and scores[neighbour[0]][neighbour[1]] is None
        ):
            yield neighbour, OPPOSITE[direction]


def find_unvisited_neighbours(maze, pos, visited):
    """Return (neighbour, direction_from_pos)"""
    for direction in (UP, RIGHT, DOWN, LEFT):
        neighbour = (pos[0] + direction[0], pos[1] + direction[1])
        if maze[neighbour[0]][neighbour[1]] != "#" and neighbour not in visited:
            yield neighbour, direction


def find_extremities(maze):
    start = end = None
    for i in range(len(maze)):
        for j in range(len(maze[i])):
            if maze[i][j] == "S":
                start = (i, j)
            elif maze[i][j] == "E":
                end = (i, j)
            if start is not None and end is not None:
                return start, end


def show(maze):
    for i in range(len(maze)):
        for j in range(len(maze[i])):
            print(maze[i][j], end="")
        print()


def show_paths(maze, tiles):
    tiles = set(tiles)
    for i in range(len(maze)):
        for j in range(len(maze[i])):
            if maze[i][j] == "#":
                print(maze[i][j], end="")
            elif (i, j) in tiles:
                print(boldred("O"), end="")
            else:
                print(".", end="")
        print()


def boldred(s):
    start = "\033[1;31m"
    end = "\033[0;0m"
    return f"{start}{s}{end}"


def read_maze(f):
    return [list(row.strip()) for row in f.readlines()]


def main():
    infile = sys.argv[1]
    with open(infile) as f:
        maze = read_maze(f)

    sys.setrecursionlimit(10000)

    start, end = find_extremities(maze)
    scores = dijkstra(maze, start, end)
    best_score = lowest_score(deepcopy(scores), start)
    print(f"Part 1: {best_score}")
    print(
        f"Part 2: {tiles_in_best_paths(deepcopy(maze), scores, start, end, best_score)}"
    )


if __name__ == "__main__":
    main()
