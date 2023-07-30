from chess import Board
from move import Move

import math
import copy
import time

import numpy as np

transposition_table = {}

def minimax(board:Board, depth:int, alpha, beta, maximizing_player) -> Move:
    if board in transposition_table:
        return transposition_table[board]
    else:
        if depth == 0 or board.game_over():
            return (board.evaluation(), None)
        if maximizing_player:
            best_move = None
            max_eval = -math.inf
            moves = board.get_legal_moves()
            for move in moves:
                sim_board = copy.deepcopy(board)
                sim_board.move(move)
                eval, _ = minimax(sim_board, depth-1, alpha, beta, False)
                if eval > max_eval:
                    max_eval = eval
                    best_move = move
                alpha = max(alpha, eval)
                if beta <= alpha:
                    break
            transposition_table[board] = max_eval, best_move
            return max_eval, best_move
        else:
            best_move = None
            min_eval = math.inf
            rotated_board = copy.deepcopy(board)
            rotated_board.rotate_board()
            enemy_moves = rotated_board.get_legal_moves()
            for enemy_move in enemy_moves:
                sim_board = copy.deepcopy(rotated_board)
                sim_board.move(enemy_move)
                sim_board.rotate_board()
                eval, _ = minimax(sim_board, depth-1, alpha, beta, True)
                if eval < min_eval:
                    min_eval = eval
                    best_move = enemy_move
                beta = min(beta, eval)
                if beta <= alpha:
                    break
            transposition_table[board] = min_eval, best_move
            return min_eval, best_move

def move_generation_test(board, depth):
    if depth == 0:
        return 1
    
    moves = board.get_legal_moves()
    numPositions = 0
    for move in moves:
        sim_board = copy.deepcopy(board)
        sim_board.move(move)
        sim_board.rotate_board()
        numPositions += move_generation_test(sim_board, depth-1)
    return numPositions

start = time.time()
print(move_generation_test(Board(), 3))
print(time.time() - start)

# ~0.7s pre bitboard