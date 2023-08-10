import time, copy, math

from chess import Position
from constants import GAME_HEAT_MAP, POSITION_TO_INDEX

def move_gen_test(position: Position, depth, white):
    if depth == 0:
        return 1

    moves = position.get_legal_moves(white)
    numPositions = 0
    hash = position.zobrist_hash
    for move in moves:
        position.make_move(move)
        numPositions += move_gen_test(position, depth-1, not white)
        position.unmake_move(move, hash)
    return numPositions



transposition_table = { "White": {}, "Black": {} }

def minimax(position:Position, depth:int, alpha, beta, maximizing_player):
    if depth == 0:
        return position.evaluation(), None
    if position.in_checkmate():
        return -math.inf, None
    if position.in_checkmate(False):
        return math.inf, None
    if position.in_fifty_move_rule_draw() or position.in_threefold_rep_draw():
        return -math.inf, None

    if position.zobrist_hash in transposition_table:
        return transposition_table["White"][position.zobrist_hash] if maximizing_player else transposition_table["Black"][position.zobrist_hash]
    else:
        if maximizing_player:
            best_move = None
            max_eval = -math.inf-1
            moves = position.get_legal_moves()
            for move in moves:
                hash = position.zobrist_hash
                position.make_move(move)
                eval, _ = minimax(position, depth-1, alpha, beta, False)
                position.unmake_move(move, hash)
                if move["code"] != 2 and move["code"] != 3:
                    eval += GAME_HEAT_MAP[move["piece"]][63-move["end"]]
                if eval > max_eval:
                    max_eval = eval
                    best_move = move
                alpha = max(alpha, eval)
                if beta <= alpha:
                    break
            # If all moves lead to checkmate, just choose 1st move
            if best_move == None:
                best_move = moves[0]
            transposition_table["White"][position.zobrist_hash] = max_eval, best_move
            return max_eval, best_move
        else:
            best_move = None
            min_eval = math.inf+1
            enemy_moves = position.get_legal_moves(False)
            for enemy_move in enemy_moves:
                hash = position.zobrist_hash
                position.make_move(enemy_move)
                eval, _ = minimax(position, depth-1, alpha, beta, True)
                position.unmake_move(enemy_move, hash)
                if enemy_move["code"] != 2 and enemy_move["code"] != 3:
                    eval -= GAME_HEAT_MAP[enemy_move["piece"]][63-enemy_move["end"]]
                if eval < min_eval:
                    min_eval = eval
                    best_move = enemy_move
                beta = min(beta, eval)
                if beta <= alpha:
                    break
            transposition_table["Black"][position.zobrist_hash] = min_eval, best_move
            return min_eval, best_move
    
b = Position()
depth = int(input("Depth: "))
b.print_board()
while True:
    #start = time.time()
    _, move = minimax(b, depth, -math.inf, math.inf, b.white_side)
    print(move)
    b.make_move(move)
    b.print_board()
    # print(f"Compute Time: {time.time() - start}")
    # b.print_board()
    # piece = input("piece: ")
    # start = POSITION_TO_INDEX[(input("start: "))]
    # end = POSITION_TO_INDEX[(input("end: "))]
    # code = int(input("code: "))
    # b.make_move({ "piece": piece, "start": start, "end": end, "captured": b._piece_at_index(end),"code": code })
