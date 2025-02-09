"""
Módulo para manejar la interfaz gráfica del juego usando Pygame.
Define colores, tamaños de casillas y funciones para dibujar el tablero.
"""

from utils import generate_moves
import pygame

# Definición de colores
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GRAY = (200, 200, 200)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
SQUARE_SIZE = 100  # Tamaño de cada casilla en píxeles


def draw_board(display, board, selected_piece=None):
    """
    Dibuja el tablero y las piezas en la pantalla.
    - display: Superficie de Pygame donde se renderiza.
    - board: Matriz 4x4 que representa el estado actual del juego.
    - selected_piece: Coordenadas (fila, columna) de la pieza seleccionada (opcional).
    """
    display.fill(WHITE)  # Fondo blanco
    for i in range(4):
        for j in range(4):
            x = j * SQUARE_SIZE + 50  # Offset para centrar el tablero
            y = i * SQUARE_SIZE + 50
            piece = board[i][j]
            color = BLACK if (i + j) % 2 == 0 else GRAY  # Alternar colores de casillas
            pygame.draw.rect(display, color, (x, y, SQUARE_SIZE, SQUARE_SIZE))

            if piece:
                # Color de la pieza: AZUL para "o", ROJO para "x"
                color = BLUE if piece.lower() == "o" else RED
                pygame.draw.circle(display, color, (x+50, y+50), 40)  # Dibujar pieza
                if piece.isupper():
                    pygame.draw.circle(display, WHITE, (x+50, y+50), 20)  # Corona para reinas

            if selected_piece and (i, j) in [move[1] for move in generate_moves(board, "x") if move[0] == selected_piece]:
                pygame.draw.circle(display, GREEN, (x+50, y+50), 15)



def get_clicked_position(event_pos):
    """
    Convierte las coordenadas del clic del mouse en posición del tablero (fila, columna).
    - event_pos: Tupla (x, y) de las coordenadas del mouse.
    Retorna: (row, col) como enteros.
    """
    x, y = event_pos
    row = (y - 50) // SQUARE_SIZE  # Ajustar al offset del tablero
    col = (x - 50) // SQUARE_SIZE
    return row, col