BOARD_SIZE = 4

def init_board():
    board = [[None for _ in range(BOARD_SIZE)] for _ in range(BOARD_SIZE)]
    board[0][1] = "o"
    board[0][3] = "o"
    board[3][0] = "x"
    board[3][2] = "x"
    return board


def print_board(board):
    print("\n#################################################\n")
    for i in range(BOARD_SIZE):
        for j in range(BOARD_SIZE):
            if board[i][j]:
                print(board[i][j], end="\t")
            else:
                print("-", end="\t")
        print("\n")
    print("\n#################################################\n")


def handle_move(board, move):

    new_board = [[cell for cell in row] for row in board]
    from_x, from_y = move[0]
    to_x, to_y = move[1]

    if move not in generate_moves(board, board[from_x][from_y].lower()):
        return board

    new_board[to_x][to_y] = new_board[from_x][from_y]
    new_board[from_x][from_y] = None

    if abs(from_x - to_x) == 2:
        mid_x = (from_x + to_x) // 2
        mid_y = (from_y + to_y) // 2
        new_board[mid_x][mid_y] = None

    if new_board[to_x][to_y] in ["o", "x"] and (
        new_board[to_x][to_y] == "o"
        and to_x == 3
        or new_board[to_x][to_y] == "x"
        and to_x == 0
    ):
        new_board[to_x][to_y] = new_board[to_x][to_y].upper()
    return new_board


def is_game_over(board):
    red_count = sum(row.count("o") + row.count("O") for row in board)
    blue_count = sum(row.count("x") + row.count("X") for row in board)
    winner = None

    if red_count == 0 or not generate_moves(board, "o"):
        winner = "x"
    if blue_count == 0 or not generate_moves(board, "x"):
        winner = "o"

    return ((red_count == 0 or
            blue_count == 0 or
            not generate_moves(board, "x") or
            not generate_moves(board, "o")),
            winner)


def generate_moves(board, player):
    MOVES = [(-1, -1), (-1, 1), (1, -1), (1, 1)]
    valid_moves = []

    def in_board(x, y):
        return 0 <= x < 4 and 0 <= y < 4

    def validate_direction(x):
        return player == "o" and x == -1 or player == "x" and x == 1

    def validate_capture(cap_x, cap_y, mid_x, mid_y):
        return (
            board[cap_x][cap_y] is None
            and board[mid_x][mid_y] is not None
            and board[mid_x][mid_y] != player
        )

    for i in range(BOARD_SIZE):
        for j in range(BOARD_SIZE):
            if board[i][j] and board[i][j].lower() == player:
                for move_x, move_y in MOVES:

                    if (
                        validate_direction(move_x)
                        and player.upper() != board[i][j]
                    ):
                        continue

                    to_x, to_y = (i + move_x, j + move_y)
                    capture_x, capture_y = ((i + move_x * 2), (j + move_y * 2))

                    if in_board(to_x, to_y) and not board[to_x][to_y]:
                        valid_moves.append(((i, j), (to_x, to_y)))

                    elif in_board(capture_x, capture_y) and validate_capture(
                        capture_x, capture_y, to_x, to_y
                    ):
                        valid_moves.append(((i, j), (capture_x, capture_y)))
    return valid_moves
