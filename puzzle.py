from typing import List, Tuple, Optional

# 15-puzzle goal state
GOAL_STATE = (
    1, 2, 3, 4,
    5, 6, 7, 8,
    9, 10, 11, 12,
    13, 14, 15, 0
)

GOAL_POS = {value: idx for idx, value in enumerate(GOAL_STATE)}

# Moves: Up, Down, Left, Right
MOVES = {
    "U": -4,
    "D": 4,
    "L": -1,
    "R": 1
}

# To avoid immediately undoing the last move
OPPOSITE = {
    "U": "D",
    "D": "U",
    "L": "R",
    "R": "L"
}


def manhattan(state: Tuple[int, ...]) -> int:
    """Compute Manhattan distance heuristic."""
    distance = 0
    for idx, tile in enumerate(state):
        if tile == 0:
            continue
        goal_idx = GOAL_POS[tile]
        x1, y1 = divmod(idx, 4)
        x2, y2 = divmod(goal_idx, 4)
        distance += abs(x1 - x2) + abs(y1 - y2)
    return distance


def is_solvable(state: Tuple[int, ...]) -> bool:
    """
    Check solvability of 15-puzzle.
    For 4x4 grid:
    - If blank is on an even row counting from bottom (2nd, 4th), inversions must be odd.
    - If blank is on an odd row counting from bottom (1st, 3rd), inversions must be even.
    """
    arr = [x for x in state if x != 0]
    inversions = 0
    for i in range(len(arr)):
        for j in range(i + 1, len(arr)):
            if arr[i] > arr[j]:
                inversions += 1

    blank_index = state.index(0)
    row_from_top = blank_index // 4
    row_from_bottom = 4 - row_from_top

    if row_from_bottom % 2 == 0:
        return inversions % 2 == 1
    return inversions % 2 == 0


def get_neighbors(state: Tuple[int, ...], last_move: Optional[str] = None):
    """Generate valid neighboring states."""
    zero_idx = state.index(0)
    row, col = divmod(zero_idx, 4)

    for move, delta in MOVES.items():
        if last_move and move == OPPOSITE[last_move]:
            continue

        new_idx = zero_idx + delta

        if move == "U" and row == 0:
            continue
        if move == "D" and row == 3:
            continue
        if move == "L" and col == 0:
            continue
        if move == "R" and col == 3:
            continue

        new_state = list(state)
        new_state[zero_idx], new_state[new_idx] = new_state[new_idx], new_state[zero_idx]
        yield move, tuple(new_state)


def ida_star(start: Tuple[int, ...]) -> Optional[List[str]]:
    """Solve the 15-puzzle using IDA* and return the move sequence."""
    if start == GOAL_STATE:
        return []

    if not is_solvable(start):
        return None

    bound = manhattan(start)
    path = [start]
    moves_path: List[str] = []

    def search(g: int, bound: int, last_move: Optional[str]) -> Tuple[int, bool]:
        current = path[-1]
        f = g + manhattan(current)

        if f > bound:
            return f, False

        if current == GOAL_STATE:
            return f, True

        min_threshold = float("inf")

        for move, neighbor in get_neighbors(current, last_move):
            if neighbor in path:
                continue

            path.append(neighbor)
            moves_path.append(move)

            temp, found = search(g + 1, bound, move)
            if found:
                return temp, True

            if temp < min_threshold:
                min_threshold = temp

            path.pop()
            moves_path.pop()

        return min_threshold, False

    while True:
        temp, found = search(0, bound, None)
        if found:
            return moves_path[:]
        if temp == float("inf"):
            return None
        bound = temp


def print_board(state: Tuple[int, ...]) -> None:
    """Print puzzle board nicely."""
    for i in range(0, 16, 4):
        row = state[i:i+4]
        print(" ".join(f"{x:2}" if x != 0 else " _" for x in row))
    print()


if __name__ == "__main__":
    # Example initial state
    start_state = (
        1, 2, 3, 4,
        5, 6, 7, 8,
        9, 10, 11, 12,
        13, 0, 14, 15
    )

    print("Initial board:")
    print_board(start_state)

    solution = ida_star(start_state)

    if solution is None:
        print("No solution exists.")
    else:
        print("Solution found!")
        print("Number of moves:", len(solution))
        print("Moves:", " ".join(solution))