from utils import is_game_over, handle_move, generate_moves


def evaluate(board):
    red_count = sum(row.count("o") + row.count("O") for row in board)
    blue_count = sum(row.count("x") + row.count("X") for row in board)
    return blue_count - red_count


def minimax(board, depth, alpha, beta, player):

    def get_sort_move_key(move):
        return evaluate(handle_move(board, move))

    if depth == 0 or is_game_over(board)[0]:
        return evaluate(board), None

    best_move = None
    if player:
        max_eval = float("-inf")
        moves = generate_moves(board, "x")
        moves = sorted(moves, key=get_sort_move_key, reverse=True)
        for move in moves:
            new_board = handle_move(board, move)
            ev, _ = minimax(new_board, depth - 1, alpha, beta, False)

            if ev > max_eval:
                max_eval = ev
                best_move = move

            alpha = max(alpha, ev)

            if beta <= alpha:
                break
        return max_eval, best_move
    else:
        min_eval = float("inf")
        moves = generate_moves(board, "o")
        moves = sorted(moves, key=get_sort_move_key)
        for move in moves:
            new_board = handle_move(board, move)
            ev, _ = minimax(new_board, depth - 1, alpha, beta, True)

            if ev < min_eval:
                min_eval = ev
                best_move
            beta = min(beta, ev)
            if beta <= alpha:
                break
        return min_eval, best_move
