from utils import init_board, handle_move, is_game_over, generate_moves, print_board
from q_learning import q_learning, load_q_table, save_q_table
from minimax import minimax
from layout import draw_board, get_clicked_position
import pygame

GRID_SIZE = 500

board = init_board()
load_q_table()

def do_q_learning_move(board):
    valid_moves = generate_moves(board, "o")
    if not valid_moves:
        return board
    new_board = q_learning(board)
    return new_board

def do_minimax_move(board):
    valid_moves = generate_moves(board, "o")
    if not valid_moves:
        return board
    _, move = minimax(board, 5, float("-inf"), float("inf"), True)
    return handle_move(board,move)

pygame.init()
screen = pygame.display.set_mode((GRID_SIZE, GRID_SIZE))
pygame.display.set_caption("Checkers and Q-Learning")
turn = "x"
selected_piece = None
running = False
while not running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = True

        if event.type == pygame.MOUSEBUTTONDOWN:
            click_x, click_y = get_clicked_position(event.pos)
            if not board[click_x][click_y] and selected_piece:
                    board = handle_move(board, (selected_piece, (click_x, click_y)))
                    selected_piece = None
                    turn = "o"

            elif board[click_x][click_y] and board[click_x][click_y].lower() == "x":
                selected_piece = click_x, click_y


    if turn == "o":
        board = do_q_learning_move(board)
        turn = "x"

    draw_board(screen, board, selected_piece)
    pygame.display.flip()
    running, _ = is_game_over(board)

save_q_table()