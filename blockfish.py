import time, copy, math

from chess import Position
from constants import GAME_HEAT_MAP, POSITION_TO_INDEX

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
        max_eval = -math.inf-1
        moves = position.get_legal_moves()
        for move in moves:
            sim_board = copy.deepcopy(position)
            sim_board.make_move(move)
            eval, _ = minimax(sim_board, depth-1, alpha, beta, False)
            if move["code"] != 2 and move["code"] != 3:
                eval += GAME_HEAT_MAP[move["piece"]][move["end"]]
            if eval > max_eval:
                max_eval = eval
                best_move = move
            alpha = max(alpha, eval)
            if beta <= alpha:
                break
        # If all moves lead to checkmate, just choose 1st move
        if best_move == None:
            best_move = moves[0]
        return max_eval, best_move
    else:
        best_move = None
        min_eval = math.inf+1
        enemy_moves = position.get_legal_moves(False)
        for enemy_move in enemy_moves:
            sim_board = copy.deepcopy(position)
            sim_board.make_move(enemy_move)
            eval, _ = minimax(sim_board, depth-1, alpha, beta, True)
            if enemy_move["code"] != 2 and enemy_move["code"] != 3:
                eval += GAME_HEAT_MAP[enemy_move["piece"]][enemy_move["end"]]
            if eval < min_eval:
                min_eval = eval
                best_move = enemy_move
            beta = min(beta, eval)
            if beta <= alpha:
                break
        # If all moves lead to checkmate, just choose 1st move
        if best_move == None:
            best_move = moves[0]
        return min_eval, best_move
    
b = Position()
depth = int(input("Depth: "))
while True:
    b.print_board()
    start = time.time()
    _, move = minimax(b, depth, -math.inf, math.inf, True)
    b.make_move(move)
    print(f"Compute Time: {time.time() - start}")
    b.print_board()
    piece = input("piece: ")
    start = POSITION_TO_INDEX[(input("start: "))]
    end = POSITION_TO_INDEX[(input("end: "))]
    code = int(input("code: "))
    b.make_move({ "piece": piece, "start": start, "end": end, "code": code })

#  WORK ON MOVE ORDERING
#  rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w - - 0 0