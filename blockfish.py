from chess import Position

import copy, math

def move_gen_test(position: Position, depth, white):
    if depth == 0:
        return 1

    moves = position.get_legal_moves(white)
    numPositions = 0
    for move in moves:
        sim_board = copy.deepcopy(position)
        sim_board.make_move(move)
        numPositions += move_gen_test(sim_board, depth-1, not white)
    return numPositions


def minimax(position:Position, depth:int, alpha, beta, maximizing_player):
    if depth == 0:
        return position.evaluation(), None
    if position.in_checkmate():
        return -math.inf, None
    if position.in_checkmate(False):
        return math.inf, None
    if position.in_fifty_move_rule_draw() or position.in_threefold_rep_draw():
        return -math.inf, None
    
    if maximizing_player:
        best_move = None
        max_eval = -math.inf
        moves = position.get_legal_moves()
        for move in moves:
            sim_board = copy.deepcopy(position)
            sim_board.make_move(move)
            eval, _ = minimax(sim_board, depth-1, alpha, beta, False)
            if eval > max_eval:
                max_eval = eval
                best_move = move
            alpha = max(alpha, eval)
            if beta <= alpha:
                break
        return max_eval, best_move
    else:
        best_move = None
        min_eval = math.inf
        enemy_moves = position.get_legal_moves(False)
        for enemy_move in enemy_moves:
            sim_board = copy.deepcopy(position)
            sim_board.make_move(enemy_move)
            eval, _ = minimax(sim_board, depth-1, alpha, beta, True)
            if eval < min_eval:
                min_eval = eval
                best_move = enemy_move
            beta = min(beta, eval)
            if beta <= alpha:
                break
        return min_eval, best_move
    
b = Position()
print(minimax(b, 3, -math.inf, math.inf, True))