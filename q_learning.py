"""
Implementación de Q-Learning como clase para el jugador "o".
"""
from utils import is_game_over, handle_move, generate_moves
from random import uniform, choice
import json

class QLearningAgent:
    def __init__(self, alpha=0.2, gamma=0.95, epsilon=1.0, q_file="q_table.json"):
        self.Q = {}  # Tabla Q: {(estado, acción): valor}
        self.Q_FILE = q_file
        self.ALPHA = alpha
        self.GAMMA = gamma
        self.EPSILON = epsilon
        self.load_q_table()

    @staticmethod
    def evaluate(self, current_board, next_board, game_over):
        """
        Calcula la recompensa con nuevos criterios estratégicos y mejor detección de vulnerabilidad.
        """
        REWARDS = {
            'win': 1500,
            'lose': -1500,
            'capture': 100,
            'king_promote': 150,
            'king_captured': -400,
            'piece_loss': -220,
            'vulnerable_penalty': -60,
            'king_difference': 80,
            'piece_difference': 40,
            'positional_advantage': 30,
            'defensive_position': 25,
            'multi_capture_potential': 50
        }

        def count_pieces(board, player):
            lower = player.lower()
            upper = player.upper()
            pieces = sum(row.count(lower) for row in board)
            kings = sum(row.count(upper) for row in board)
            return pieces + kings, kings

        def get_vulnerable_count(board, player):
            vulnerable = 0
            for i in range(4):
                for j in range(4):
                    if board[i][j] and board[i][j].lower() == player.lower():
                        vulnerable += self.is_vulnerable(board, i, j, player)
            return vulnerable

        def is_vulnerable(self, board, row, col, player):
            enemy = 'x' if player.lower() == 'o' else 'o'
            attack_dirs = [(-1,-1), (-1,1), (1,-1), (1,1)] if board[row][col].isupper() else (
                [(-1,-1), (-1,1)] if player == 'o' else [(1,-1), (1,1)]
            )
            
            for dx, dy in attack_dirs:
                if 0 <= row+dx < 4 and 0 <= col+dy < 4:
                    if board[row+dx][col+dy].lower() == enemy:
                        if 0 <= row-dx < 4 and 0 <= col-dy < 4:
                            if board[row-dx][col-dy] is None:
                                return 1
            return 0

        # Cálculo de métricas mejorado
        current_o_pieces, current_o_kings = count_pieces(current_board, 'o')
        next_o_pieces, next_o_kings = count_pieces(next_board, 'o')
        
        reward = 0

        if game_over:
            _, winner = is_game_over(next_board)
            return REWARDS['win'] if winner == 'o' else REWARDS['lose']

        # Diferencias clave
        piece_diff = (next_o_pieces - current_o_pieces) * REWARDS['piece_difference']
        king_diff = (next_o_kings - current_o_kings) * REWARDS['king_difference']
        reward += piece_diff + king_diff

        # Eventos de captura y promoción
        reward += (current_o_pieces - next_o_pieces) * REWARDS['piece_loss']
        reward += (next_o_kings - current_o_kings) * REWARDS['king_promote']
        
        # Ventaja posicional mejorada
        defensive_positions = [(0,1), (0,3), (3,0), (3,2)]
        defensive_score = sum(1 for i,j in defensive_positions if next_board[i][j] and next_board[i][j].lower() == 'o')
        reward += defensive_score * REWARDS['defensive_position']

        # Potencial de captura múltiple
        multi_capture = sum(1 for move in generate_moves(next_board, 'o') if abs(move[0][0]-move[1][0]) > 1)
        reward += multi_capture * REWARDS['multi_capture_potential']

        return reward

    def update_Q_table(self, state, action, reward, next_state, next_moves):
        """Actualiza la Q-table usando la ecuación de Bellman."""
        max_future = max([self.Q.get((next_state, m), 0) for m in next_moves], default=0)
        current = self.Q.get((state, action), 0)
        self.Q[(state, action)] = current + self.ALPHA * (reward + self.GAMMA * max_future - current)

    def get_action(self, state, moves):
        """Elige una acción usando epsilon-greedy."""
        if uniform(0, 1) < self.EPSILON:
            return choice(moves)  # Exploración
        else:
            Q_vals = [self.Q.get((state, move), 0) for move in moves]
            max_Q = max(Q_vals)
            return choice([move for i, move in enumerate(moves) if Q_vals[i] == max_Q])

    def board_to_state(self, board):
        """Serialización única del estado del tablero"""
        state = []
        for row in board:
            for cell in row:
                state.append(str(cell) if cell else '-')
        return ''.join(state)

    def perform_move(self, board):
        """Ejecuta un paso de Q-Learning y retorna el nuevo tablero."""
        state = self.board_to_state(board)
        moves = generate_moves(board, "o")
        if not moves:
            return board
            
        action = self.get_action(state, moves)
        new_board = handle_move(board, action)
        next_state = str(new_board)
        next_moves = generate_moves(new_board, "x")
        game_over, _ = is_game_over(new_board)
        
        reward = self.evaluate(self, board, new_board, game_over)
        self.update_Q_table(state, action, reward, next_state, next_moves)
        return new_board

    def variate_epsilon(self, episode):
        """Reduce epsilon gradualmente."""
        self.EPSILON = max(0.1, 0.9 ** (episode % 100))
        return self.EPSILON

    def load_q_table(self):
        """Carga la Q-table desde un archivo JSON."""
        try:
            with open(self.Q_FILE, "r") as file:
                self.Q = {tuple(eval(k)): v for k, v in json.load(file).items()}
        except FileNotFoundError:
            self.Q = {}

    def save_q_table(self):
        """Guarda la Q-table en un archivo JSON."""
        with open(self.Q_FILE, "w") as f:
            json.dump({str(k): v for k, v in self.Q.items()}, f)