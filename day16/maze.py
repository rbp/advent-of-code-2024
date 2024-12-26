from copy import deepcopy
import heapq
import sys

UP = (-1, 0)
RIGHT = (0, 1)
DOWN = (1, 0)
LEFT = (0, -1)

OPPOSITE = {UP: DOWN, DOWN: UP, LEFT: RIGHT, RIGHT: LEFT}


def lowest_score(maze):
    # show(maze)
    start, end = find_extremities(maze)
    scores = dijkstra(maze, start, end)

    return scores[start[0]][end[0]][0]


def dijkstra(maze, start, end):
    # scores[x][y] = (score, direction) | None
    scores = [[None] * len(maze[0]) for _ in maze]

    scores[end[0]][end[1]] = (0, None)
    # To be able to heapify it, unvisited is a list of (score, position)
    reached_start = False
    unvisited = [(0, end)]
    while unvisited and not reached_start:
        node_score, node_pos = heapq.heappop(unvisited)
        # Update the neighbours' scores
        for neighbour, direction_to_node in neighbours(maze, node_pos, scores):
            node_score, node_direction = scores[node_pos[0]][node_pos[1]]
            cost_move = node_score + 1
            if (
                (node_direction is not None and node_direction != direction_to_node)
                or neighbour == start
                and direction_to_node != RIGHT
            ):
                cost_move += 1000
            scores[neighbour[0]][neighbour[1]] = (cost_move, direction_to_node)
            heapq.heappush(unvisited, (cost_move, neighbour))

            # If node == start, we can stop
            if neighbour == start:
                reached_start = True

    return scores


def neighbours(maze, pos, scores):
    for direction in (UP, RIGHT, DOWN, LEFT):
        new_pos = (pos[0] + direction[0], pos[1] + direction[1])
        if (
            maze[new_pos[0]][new_pos[1]] != "#"
            and scores[new_pos[0]][new_pos[1]] is None
        ):
            yield new_pos, OPPOSITE[direction]


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


def read_maze(f):
    return [list(row.strip()) for row in f.readlines()]


def main():
    infile = sys.argv[1]
    with open(infile) as f:
        maze = read_maze(f)

    print(f"Part 1: {lowest_score(deepcopy(maze))}")


if __name__ == "__main__":
    main()
