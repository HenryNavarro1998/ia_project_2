"""
Script de entrenamiento para el agente de Q-Learning contra un oponente (Minimax/aleatorio).
Ejecuta múltiples episodios de juego para entrenar la Q-table y registra estadísticas de rendimiento.
"""

from utils import init_board, handle_move, is_game_over, generate_moves
from q_learning import QLearningAgent
from minimax import minimax
from collections import defaultdict
import random

EPISODES = 1000  # Número total de partidas de entrenamiento

def do_minimax_move(board):
    """
    Realiza un movimiento para el jugador 'x' usando Minimax o selección aleatoria.

    Args:
        board (list): Estado actual del tablero

    Returns:
        list: Nuevo estado del tablero después del movimiento
    """
    valid_moves = generate_moves(board, "x")
    if not valid_moves:
        return board

    # Versión 1: Minimax con profundidad 1 (descomentar para usar)
    # _, move = minimax(board, 1, float("-inf"), float("inf"), True)

    # Versión 2: Movimiento aleatorio (usado actualmente)
    move = random.choice(valid_moves)

    return handle_move(board, move)

def do_q_learning_move(board, q_agent):
    """
    Realiza un movimiento para el jugador 'o' usando Q-Learning.

    Args:
        board (list): Estado actual del tablero
        q_agent (QLearningAgent): Instancia del agente entrenado

    Returns:
        list: Nuevo estado del tablero después del movimiento
    """
    valid_moves = generate_moves(board, "o")
    return q_agent.perform_move(board) if valid_moves else board

# Configuración inicial del entrenamiento
board = init_board()  # Tablero inicial
results = defaultdict(int)  # Registro de resultados: {'o', 'x', 'draw'} -> conteo
q_agent = QLearningAgent()  # Instancia del agente Q-Learning
q_agent.load_q_table()  # Cargar Q-table existente (si hay)

# Variables de control del entrenamiento
episode = 0  # Contador de partidas completadas
turns = 0  # Contador de turnos por partida (máximo 64)
player_turn = "x"  # Jugador que inicia (x: Minimax/aleatorio, o: Q-Learning)

# Bucle principal de entrenamiento
while episode < EPISODES:
    # Alternancia de turnos entre jugadores
    if player_turn == "x":
        board = do_minimax_move(board)
        player_turn = "o"
    else:
        board = do_q_learning_move(board, q_agent)
        player_turn = "x"

    turns += 1

    # Verificar condiciones de término de la partida
    game_over, winner = is_game_over(board)
    if game_over or turns >= 64:  # Límite de 64 turnos para evitar loops
        # Registrar resultados
        final_result = winner if winner else "draw"
        results[final_result] += 1
        
        # Reiniciar variables para nueva partida
        board = init_board()
        turns = 0
        episode += 1
        player_turn = "x"
        
        # Actualizar épsilon (exploración vs explotación)
        current_epsilon = q_agent.variate_epsilon(episode)
        
        # Log de progreso
        print(
            f"Episodio: {episode}/{EPISODES} | "
            f"Victorias Q: {results['o']} ({results['o']/episode*100:.1f}%) | "
            f"Derrotas: {results['x']} | "
            f"Empates: {results['draw']} | "
            f"Épsilon: {current_epsilon:.3f}"
        )

# Finalización del entrenamiento
print("\nResultados finales del entrenamiento:")
print(f"• Victorias del agente Q-Learning: {results['o']}")
print(f"• Derrotas del agente Q-Learning: {results['x']}")
print(f"• Empates: {results['draw']}")
q_agent.save_q_table()  # Guardar la Q-table entrenada