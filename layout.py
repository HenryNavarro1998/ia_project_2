from utils import generate_moves
import pygame

BLACK = (0, 0 ,0)
WHITE = (255, 255, 255)
GRAY = (200, 200, 200)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
SQUARE_SIZE = 100

def draw_board(display, board, selected_piece=None):
    display.fill(WHITE)
    for i in range(4):
        for j in range(4):
            x = j * SQUARE_SIZE + 50
            y = i * SQUARE_SIZE + 50
            piece = board[i][j]
            color = BLACK if (i + j) % 2 == 0 else GRAY
            pygame.draw.rect(display, color, (x, y, SQUARE_SIZE, SQUARE_SIZE))

            if piece:
                color = BLUE if piece.lower() == "o" else RED
                pygame.draw.circle(display, color, (x+50, y+50), 40)
                if piece.isupper():
                    pygame.draw.circle(display, WHITE, (x+50, y+50), 20)
                if selected_piece:
                    print(selected_piece)
                    pass

def get_clicked_position(event_pos):
    x, y = event_pos
    row = (y - 50) // SQUARE_SIZE
    col = (x - 50) // SQUARE_SIZE
    return row, col
