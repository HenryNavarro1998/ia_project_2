"""
Implementación del algoritmo Minimax con poda alfa-beta para el jugador "x".
"""
from utils import is_game_over, handle_move, generate_moves

def evaluate(board):
    """Evalúa el tablero: diferencia entre piezas azules ("x") y rojas ("o")."""
    red_count = sum(row.count("o") + row.count("O") for row in board)
    blue_count = sum(row.count("x") + row.count("X") for row in board)
    return blue_count - red_count  # Valor positivo favorece a "x"

def minimax(board, depth, alpha, beta, player):
    """
    Algoritmo Minimax con poda alfa-beta.
    - board: Estado actual del tablero.
    - depth: Profundidad máxima de búsqueda.
    - alpha: Valor alfa para poda.
    - beta: Valor beta para poda.
    - player: True para maximizar ("x"), False para minimizar ("o").
    Retorna: (valor de evaluación, mejor movimiento)
    """
    def get_sort_move_key(move):
        """Ordena movimientos para optimizar la poda."""
        return evaluate(handle_move(board, move))

    if depth == 0 or is_game_over(board)[0]:
        return evaluate(board), None  # Caso base

    best_move = None
    if player:  # Maximizar (jugador "x")
        max_eval = float("-inf")
        moves = sorted(generate_moves(board, "x"), key=get_sort_move_key, reverse=True)
        for move in moves:
            new_board = handle_move(board, move)
            ev, _ = minimax(new_board, depth-1, alpha, beta, False)
            if ev > max_eval:
                max_eval, best_move = ev, move
            alpha = max(alpha, ev)
            if beta <= alpha:
                break  # Poda beta
        return max_eval, best_move
    else:  # Minimizar (jugador "o")
        min_eval = float("inf")
        moves = sorted(generate_moves(board, "o"), key=get_sort_move_key)
        for move in moves:
            new_board = handle_move(board, move)
            ev, _ = minimax(new_board, depth-1, alpha, beta, True)
            if ev < min_eval:
                min_eval, best_move = ev, move
            beta = min(beta, ev)
            if beta <= alpha:
                break  # Poda alfa
        return min_eval, best_move