from utils import init_board, handle_move, is_game_over, print_board, generate_moves
from q_learning import q_learning, load_q_table, save_q_table, variate_epsilon, EPSILON
from minimax import minimax
from collections import defaultdict
import random

EPISODES = 1000


def do_minimax_move(board):
    valid_moves = generate_moves(board, "x")
    if not valid_moves:
        return board
    # _, move = minimax(board, 1, float("-inf"), float("inf"), True)
    move = random.choice(valid_moves)
    return handle_move(board, move)

def do_q_learning_move(board):
    valid_moves = generate_moves(board, "o")
    if not valid_moves:
        return board
    new_board = q_learning(board)
    return new_board

board = init_board()
results = defaultdict(int)
player_turn = "x"
turns = 0
episode = 0

load_q_table()

while episode < EPISODES:
    # print_board(board)
    if player_turn == "x":
        board = do_minimax_move(board)
        player_turn = "o"
    else:
        board = do_q_learning_move(board)
        player_turn = "x"
    turns += 1

    game, winner = is_game_over(board)
    if game or turns == 64:
        winner = winner if winner else "draw"
        results[winner] += 1
        board = init_board()
        turns = 0
        episode += 1
        player_turn = "x"
        print(f"Statistics: Games: {episode}, Win: {results['o']} = {round((results['o']/episode) * 100, 2)}%, Lose: {results['x']} = {round((results['x']/episode) * 100, 2)}%, Draw: {results['draw']} = {round((results['draw']/episode) * 100, 2)}% - Epsilon: {variate_epsilon(episode)}")

print("%s" %results)
save_q_table()
