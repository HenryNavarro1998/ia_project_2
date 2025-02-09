from utils import is_game_over, handle_move, generate_moves
from random import uniform, choice
import json

Q = {}
Q_FILE = "q_table.json"
ALPHA = 0.2
GAMMA = 0.95
EPSILON = 1.0

def evaluate(current_board, next_board, game_over):
    # Configuración de pesos y recompensas
    REWARDS = {
        'win': 1000,
        'lose': -1000,
        'capture': 80,
        'king_promote': 120,
        'king_captured': -150,
        'piece_loss': -100,
        'vulnerable_penalty': -40,
        'king_difference': 60,
        'piece_difference': 30,
        'positional_advantage': 20
    }

    def count_pieces(board, player):
        """Cuenta piezas normales y reinas para un jugador"""
        lower = player.lower()
        upper = player.upper()
        pieces = sum(row.count(lower) for row in board)
        kings = sum(row.count(upper) for row in board)
        return pieces + kings, kings  # Total piezas, reinas

    def get_vulnerable_count(board, player):
        """Cuenta piezas vulnerables del jugador"""
        vulnerable = 0
        for i in range(4):
            for j in range(4):
                if board[i][j] and board[i][j].lower() == player.lower() and is_vulnerable(board, i, j, player):
                    vulnerable += 1
        return vulnerable

    def is_vulnerable(board, row, col, player):
        """Determina si una pieza está en posición vulnerable"""
        enemy = 'x' if player.lower() == 'o' else 'o'
        enemy_kings = enemy.upper()
        
        # Direcciones de ataque según tipo de pieza
        attack_dirs = []
        if board[row][col].islower():  # Pieza normal
            attack_dirs = [(-1, -1), (-1, 1)] if player == 'o' else [(1, -1), (1, 1)]
        else:  # Reina
            attack_dirs = [(-1, -1), (-1, 1), (1, -1), (1, 1)]

        for dx, dy in attack_dirs:
            adj_row = row + dx
            adj_col = col + dy
            jump_row = row + 2*dx
            jump_col = col + 2*dy

            if 0 <= adj_row < 4 and 0 <= adj_col < 4:
                attacker = board[adj_row][adj_col]
                if attacker and attacker.lower() == enemy or attacker == enemy_kings:
                    if 0 <= jump_row < 4 and 0 <= jump_col < 4:
                        if board[jump_row][jump_col] == '.':
                            return True
        return False

    # Calculamos métricas para el estado actual y siguiente
    current_o_pieces, current_o_kings = count_pieces(current_board, 'o')
    current_x_pieces, current_x_kings = count_pieces(current_board, 'x')
    
    next_o_pieces, next_o_kings = count_pieces(next_board, 'o')
    next_x_pieces, next_x_kings = count_pieces(next_board, 'x')
    
    reward = 0

    # Recompensas inmediatas por victoria/derrota
    if game_over:
        game_over, winner = is_game_over(next_board)
        reward += REWARDS['win'] if winner == 'o' else REWARDS['lose']
        return reward  # Terminamos evaluación si hay ganador

    # Diferencial de piezas
    piece_diff = (next_o_pieces - next_x_pieces) - (current_o_pieces - current_x_pieces)
    reward += piece_diff * REWARDS['piece_difference']
    
    # Diferencial de reinas
    king_diff = (next_o_kings - next_x_kings) - (current_o_kings - current_x_kings)
    reward += king_diff * REWARDS['king_difference']

    # Eventos de captura y promoción
    captured_pieces = (current_x_pieces - next_x_pieces)
    reward += captured_pieces * REWARDS['capture']
    
    lost_pieces = (current_o_pieces - next_o_pieces)
    reward += lost_pieces * REWARDS['piece_loss']
    
    # Coronaciones de reyes
    new_kings = next_o_kings - current_o_kings
    reward += new_kings * REWARDS['king_promote']
    
    lost_kings = current_o_kings - next_o_kings
    reward += lost_kings * REWARDS['king_captured']

    # Vulnerabilidad de piezas
    vulnerable_o = get_vulnerable_count(next_board, 'o')
    reward += vulnerable_o * REWARDS['vulnerable_penalty']
    
    vulnerable_x = get_vulnerable_count(next_board, 'x')
    reward -= vulnerable_x * REWARDS['vulnerable_penalty']  # Beneficio si enemigo vulnerable

    # Ventaja posicional (control del centro)
    center_positions = [(1,1), (1,2), (2,1), (2,2)]
    center_control = sum(1 for i,j in center_positions if next_board[i][j] and next_board[i][j].lower() == 'o')
    reward += center_control * REWARDS['positional_advantage']

    return reward


def update_Q_table(state, action, reward, next_state, next_moves):
    max_future = max([Q.get((next_state, m), 0) for m in next_moves], default=0)
    current = Q.get((state, action), 0)
    Q[(state, action)] = current + ALPHA * (reward + GAMMA*max_future - current)


def get_action(state, moves):
    if uniform(0, 1) < EPSILON:
        return choice(moves)
    Q_vals = [Q.get((state, move), 0) for move in moves]
    max_Q = max(Q_vals)
    best_moves = [move for i, move in enumerate(moves) if Q_vals[i] == max_Q]
    return choice(best_moves)


def q_learning(board):
    state = str(board)
    moves = generate_moves(board, "o")
    action = get_action(state, moves)
    new_board = handle_move(board, action)
    next_state = str(new_board)
    next_moves = generate_moves(new_board, "x")
    game_over, _ = is_game_over(new_board)
    reward = evaluate(board, new_board, game_over)
    update_Q_table(state, action, reward, next_state, next_moves)
    return new_board

def variate_epsilon(episode):
    global EPSILON
    EPSILON = max(0.1, 0.9 ** (episode % 500))
    return EPSILON

def load_q_table():
    global Q
    try:
        with open(Q_FILE, "r") as file:
            Q = json.load(file)
            Q = {tuple(eval(key)): value for key, value in Q.items()}
    except FileNotFoundError:
        Q = {}


def save_q_table():
    try:
        with open(Q_FILE, "w") as f:
            json.dump({str(key): value for key, value in Q.items()}, f)
    except Exception as e:
        print("Error guardando Q-table:", e)