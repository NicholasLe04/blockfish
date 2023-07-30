from move import Move, POSITION_MAPPING

import numpy as np
import time, random, copy, math


KNIGHT_DIRECTIONS = [ -25, -23, -10, 14, 25, 23, 10, -14 ]
BISHOP_DIRECTIONS = [ -13, -11, 11, 13 ]
ROOK_DIRECTIONS = [ -1, -12, 1, 12 ]
QUEEN_DIRECTIONS = ROOK_DIRECTIONS + BISHOP_DIRECTIONS
KING_DIRECTIONS = ROOK_DIRECTIONS + BISHOP_DIRECTIONS

PIECE_VALUES = { 
                ' ': 0, 'P': 1, 'N': 3.05, 'B': 3.33, 'R': 5.63, 'Q': 9.5, 'K': 0 , 
                'p': -1, 'n': -3.05, 'b':- 3.33, 'r': -5.63, 'q': -9.5, 'k': 0 
                } # Per AlphaZero

class Board():

    # [0,   1,   2,   3,   4,   5,   6,   7,   8,   9,   10,  11, 
    # 12,  13,  14,  15,  16,  17,  18,  19,  20,  21,  22,  23, 
    # 24,  25,  26,  27,  28,  29,  30,  31,  32,  33,  34,  35, 
    # 36,  37,  38,  39,  40,  41,  42,  43,  44,  45,  46,  47, 
    # 48,  49,  50,  51,  52,  53,  54,  55,  56,  57,  58,  59, 
    # 60,  61,  62,  63,  64,  65,  66,  67,  68,  69,  70,  71, 
    # 72,  73,  74,  75,  76,  77,  78,  79,  80,  81,  82,  83, 
    # 84,  85,  86,  87,  88,  89,  90,  91,  92,  93,  94,  95, 
    # 96,  97,  98,  99,  100, 101, 102, 103, 104, 105, 106, 107, 
    # 108, 109, 110, 111, 112, 113, 114, 115, 116, 117, 118, 119, 
    # 120, 121, 122, 123, 124, 125, 126, 127, 128, 129, 130, 131,
    # 132, 133, 134, 135, 136, 137, 138, 139, 140, 141, 142, 143]

    def __init__(self):
        self.board = np.array([
            'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 
            'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 
            'X', 'X', 'r', 'n', 'b', 'q', 'k', 'b', 'n', 'r', 'X', 'X', 
            'X', 'X', 'p', 'p', 'p', 'p', 'p', 'p', 'p', 'p', 'X', 'X', 
            'X', 'X', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', 'X', 'X', 
            'X', 'X', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', 'X', 'X', 
            'X', 'X', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', 'X', 'X', 
            'X', 'X', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', 'X', 'X', 
            'X', 'X', 'P', 'P', 'P', 'P', 'P', 'P', 'P', 'P', 'X', 'X', 
            'X', 'X', 'R', 'N', 'B', 'Q', 'K', 'B', 'N', 'R', 'X', 'X', 
            'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 
            'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 
        ], dtype=str)

        self.ep_vulnerable_index = None
        self.white_side = True
        self.castle_availablity = { "king_side_clear": False, "queen_side_clear": False, "king_side_possible": True, "queen_side_possible": True}
        self.enemy_castle_availability = { "king_side_clear": False, "queen_side_clear": False, "king_side_possible": True, "queen_side_possible": True}
        self.move_stack = list()
        self.fifty_move_rule_counter = 0
    
    def from_FEN(self, fen:str):
        pieces = fen.split(' ')[0]
        active_side = fen.split(' ')[1]
        castling = fen.split(' ')[2]
        ep_idx = fen.split(' ')[3]
        fifty_rule_counter = fen.split(' ')[4]

        # Update Pieces
        piece_list = list()
        for i in range(len(pieces)):
            if pieces[i].isalpha():
                piece_list.append(pieces[i])
            elif pieces[i].isdigit():
                empty_squares = list()
                for _ in range(int(pieces[i])):
                    empty_squares.append(' ')
                piece_list += empty_squares

        self.board[26:34] = piece_list[0:8]
        self.board[38:46] = piece_list[8:16]
        self.board[50:58] = piece_list[16:24]
        self.board[62:70] = piece_list[24:32]
        self.board[74:82] = piece_list[32:40]
        self.board[86:94] = piece_list[40:48]
        self.board[98:106] = piece_list[48:56]
        self.board[110:118] = piece_list[56:64]

        # Update active_side
        if active_side == 'w':
            self.white_side = True
        else: 
            self.white_side = False

        # Update castling
        if castling == '-':
            self.castle_availablity = { "king_side_clear": False, "queen_side_clear": False, "king_side_possible": True, "queen_side_possible": True}
            self.enemy_castle_availability = { "king_side_clear": False, "queen_side_clear": False, "king_side_possible": True, "queen_side_possible": True}
        else:
            self.castle_availablity["king_side_possible"] = False
            self.castle_availablity["queen_side_possible"] = False
            self.enemy_castle_availability["king_side_possible"] = False
            self.enemy_castle_availability["queen_side_possible"] = False
            for el in castling:
                if el == 'K':
                    self.castle_availablity["king_side_possible"] = True
                elif el == 'Q':
                    self.castle_availablity["queen_side_possible"] = True
                elif el == 'k':
                    self.enemy_castle_availability["king_side_possible"] = True
                else:
                    self.enemy_castle_availability["queen_side_possible"] = True
            self._update_castle_availability()

        # Update en passant vulnerability
        if ep_idx == '-':
            self.ep_vulnerable_index = None
        else:
            for key, value in POSITION_MAPPING.items():
                if ep_idx == value:
                    self.fifty_move_rule_counter = key
                    break
            
        # Update Fifty Rule Counter
        self.fifty_move_rule_counter = int(fifty_rule_counter)

    def print_board(self):
        row = 8
        for i in range(26, 122, 12):
            print("+---+---+---+---+---+---+---+---+")
            print(f"| {self.board[i]} | {self.board[i+1]} | {self.board[i+2]} | {self.board[i+3]} | {self.board[i+4]} | {self.board[i+5]} | {self.board[i+6]} | {self.board[i+7]} | {row}")
            row -= 1
        print("+---+---+---+---+---+---+---+---+\n  a   b   c   d   e   f   g   h  ")

    def rotate_board(self):
        '''Switches to black piece perspective'''
        self.white_side = not self.white_side
        self.board = np.flip(self.board)
        for i in range(26, 118):
            piece = self.board[i]
            if piece != ' ' and piece != 'X':
                self.board[i] = piece.swapcase()

        if self.ep_vulnerable_index is not None:
            self.ep_vulnerable_index = 143 - self.ep_vulnerable_index 

        tmp = self.castle_availablity
        self.castle_availablity = self.enemy_castle_availability
        self.enemy_castle_availability = tmp

    def evaluation(self) -> float:
        if self.giving_checkmate():
            return math.inf
        if self.in_checkmate():
            return -math.inf
        if self.in_threefold_rep_draw():
            return 0
        if self.in_fifty_move_rule_draw():
            return 0
        eval = 0
        for row in range(26, 122, 12):
            for col in range(8):
                eval += PIECE_VALUES[self.board[row+col]] 
        return round(eval, 2)

    def _update_castle_availability(self):
        if self.castle_availablity["king_side_possible"] and self.castle_availablity["queen_side_possible"]:
            self.castle_availablity["king_side_clear"] = False
            self.castle_availablity["queen_side_clear"] = False
            if self.board[117] != 'R':
                self.castle_availablity["king_side_possible"] = False
            if self.board[110] != 'R':
                self.castle_availablity["queen_side_possible"] = False
            if self.white_side: 
                if self.castle_availablity["king_side_possible"] and (self.board[115:117] == [' ', ' ']).all():
                    self.castle_availablity["king_side_clear"] = True
                if self.castle_availablity["queen_side_possible"] and (self.board[111:114] == [' ', ' ', ' ']).all():
                    self.castle_availablity["queen_side_clear"] = True
            else:
                if self.castle_availablity["king_side_possible"] and (self.board[111:113] == [' ', ' ']).all():
                    self.castle_availablity["king_side_clear"] = True
                if self.castle_availablity["queen_side_possible"] and (self.board[114:117] == [' ', ' ', ' ']).all():
                    self.castle_availablity["queen_side_clear"] = True
  
    def move(self, move:Move):
        self.move_stack.append(move)

        # Fifty-move rule
        if move.type == 'castle':
            self.fifty_move_rule_counter += 1
        elif (self.board[move.end_idx] == ' ' and self.board[move.start_idx] != 'P'):
            self.fifty_move_rule_counter += 1
        else:
            self.fifty_move_rule_counter == 0

        if move.type == 'standard' or move.type == 'capture': # Standard move
            if self.board[move.start_idx] == 'K':
                self.castle_availablity["king_side_possible"] = False
                self.castle_availablity["queen_side_possible"] = False
            if self.castle_availablity["king_side_possible"]:
                if self.board[move.start_idx] == 'R' and ((move.start_idx == 117 and self.white_side) or (move.start_idx == 110 and not self.white_side)):
                    self.castle_availablity["king_side_possible"] = False
            if self.castle_availablity["queen_side_possible"]:
                if self.board[move.start_idx] == 'R' and ((move.start_idx == 110 and self.white_side) or (move.start_idx == 117 and not self.white_side)):
                    self.castle_availablity["queen_side_possible"] = False
            self.board[move.end_idx] = self.board[move.start_idx]
            self.board[move.start_idx] = ' '
        elif move.type == 'en passant': # En Passant Capture
            self.board[self.ep_vulnerable_index] = self.board[move.start_idx]
            self.board[move.start_idx] = ' '
            self.board[self.ep_vulnerable_index+12] = ' ' 
        elif move.type == 'castle':
            if self.white_side:
                if move.castle_side == 'Q':
                    self.board[110:115] = [' ', ' ', ' ', ' ', ' ']
                    self.board[113] = 'R'
                    self.board[112] = 'K'
                else:
                    self.board[114:118] = [' ', ' ', ' ', ' ']
                    self.board[115] = 'R'
                    self.board[116] = 'K'
            else:
                if move.castle_side == 'Q':
                    self.board[113:118] = [' ', ' ', ' ', ' ', ' ']
                    self.board[115] = 'R'
                    self.board[116] = 'K'
                else:
                    self.board[110:114] = [' ', ' ', ' ', ' ']
                    self.board[113] = 'R'
                    self.board[112] = 'K'
        elif move.type == 'first pawn':
            self.board[move.end_idx] = self.board[move.start_idx]
            self.board[move.start_idx] = ' '
            self.ep_vulnerable_index = move.ep_idx 
        elif move.type == 'promotion':
            self.board[move.start_idx] = ' '
            self.board[move.end_idx] = move.new_piece
        
        if move.type != 'first pawn':
            self.ep_vulnerable_index = None # Reset en passant
    

        self._update_castle_availability()

    def get_legal_moves(self, captures_only:bool=False):
        pseudo_legal_moves = (
            self._get_legal_pawn_moves(captures_only=captures_only) + 
            self._get_legal_knight_moves(captures_only=captures_only) + 
            self._get_legal_bishop_moves(captures_only=captures_only) + 
            self._get_legal_rook_moves(captures_only=captures_only) + 
            self._get_legal_queen_moves(captures_only=captures_only) + 
            self._get_legal_king_moves(captures_only=captures_only)
        )
        legal_moves = []
        for move in pseudo_legal_moves:
            if not((move.type == 'capture' or move.type == 'promotion') and self.board[move.end_idx] == 'k'):
                legal_moves.append(move)

        return legal_moves

    def _get_legal_pawn_moves(self, captures_only:bool):
        legal_pawn_moves = list()
        pawns_found = 0
        for i in range(26,118):
            piece = self.board[i]
            if piece == 'P':
                pawns_found += 1
                row = i//12
                # Forward Movement
                if self.board[i-12] == ' ' and not captures_only:
                    legal_pawn_moves.append(Move(type="standard", start=i, end=i-12))
                    if self.board[i-24] == ' ' and row == 8:
                        legal_pawn_moves.append(Move(type="first pawn", start=i, end=i-24, ep_idx=i-12))
                # Left Diagonal Capture
                if self.board[i-13].islower():
                    legal_pawn_moves.append(Move(type="capture", start=i, end=i-13))
                # En passant to the left
                elif i-13 == self.ep_vulnerable_index:
                    legal_pawn_moves.append(Move(type="en passant", start=i, end=i-13, ep_idx=i-13))
                # Right Diagonal Capture
                if self.board[i-11].islower():
                    legal_pawn_moves.append(Move(type="capture", start=i, end=i-11))
                # En passant to the right
                elif i-11 == self.ep_vulnerable_index:
                    legal_pawn_moves.append(Move(type="en passant", start=i, end=i-11, ep_idx=i-11))

                # DEAL WITH PROMOTION   
                if row == 3:
                    j = len(legal_pawn_moves) - 1
                    while (j >= 0 and legal_pawn_moves[j].start_idx == i):
                        altered_move = legal_pawn_moves.pop(j)
                        legal_pawn_moves.append(Move(type='promotion', start=altered_move.start_idx, end=altered_move.end_idx, new_piece='N'))
                        legal_pawn_moves.append(Move(type='promotion', start=altered_move.start_idx, end=altered_move.end_idx, new_piece='B'))
                        legal_pawn_moves.append(Move(type='promotion', start=altered_move.start_idx, end=altered_move.end_idx, new_piece='R'))
                        legal_pawn_moves.append(Move(type='promotion', start=altered_move.start_idx, end=altered_move.end_idx, new_piece='Q'))
                        j -= 1
                    
                if pawns_found == 8:
                    break
        return(legal_pawn_moves)

    def _get_legal_knight_moves(self, captures_only:bool):
        legal_knight_moves = list()
        knights_found = 0
        for i in range(26,118):
            if self.board[i] == "N":
                for direction in KNIGHT_DIRECTIONS:
                    if self.board[i+direction] == ' ' and not captures_only:
                        legal_knight_moves.append(Move(type="standard", start=i, end=i+direction))
                    elif self.board[i+direction].islower():
                        legal_knight_moves.append(Move(type="capture", start=i, end=i+direction))
                if knights_found == 2:
                    break
        return legal_knight_moves
            
    def _get_legal_bishop_moves(self, captures_only:bool):
        legal_bishop_moves = list()
        bishops_found = 0
        for i in range(26,118):
            if self.board[i] == "B":
                bishops_found += 1
                for direction in BISHOP_DIRECTIONS:
                    current_square = i
                    while (self.board[current_square+direction] == ' '):
                        if not captures_only:
                            legal_bishop_moves.append(Move(type="standard", start=i, end=current_square+direction))
                        current_square = current_square+direction
                    if self.board[current_square+direction].islower():
                        legal_bishop_moves.append(Move(type="capture", start=i, end=current_square+direction))
                if bishops_found == 2: 
                    break
        return legal_bishop_moves

    def _get_legal_rook_moves(self, captures_only:bool):
        legal_rook_moves = list()
        rooks_found = 0
        for i in range(26,118):
            if self.board[i] == "R":
                rooks_found += 1
                for direction in ROOK_DIRECTIONS:
                    current_square = i
                    while (self.board[current_square+direction] == ' '):
                        if not captures_only:
                            legal_rook_moves.append(Move(type="standard", start=i, end=current_square+direction))
                        current_square = current_square+direction
                    if self.board[current_square+direction].islower():
                        legal_rook_moves.append(Move(type="capture", start=i, end=current_square+direction))
                if rooks_found == 2:
                    break
        return legal_rook_moves

    def _get_legal_queen_moves(self, captures_only:bool):
        legal_queen_moves = list()
        for i in range(26,118):
            if self.board[i] == "Q":
                for direction in QUEEN_DIRECTIONS:
                    current_square = i
                    while (self.board[current_square+direction] == ' '):
                        if not captures_only:
                            legal_queen_moves.append(Move(type="standard", start=i, end=current_square+direction))
                        current_square = current_square+direction
                    if self.board[current_square+direction].islower():
                        legal_queen_moves.append(Move(type="capture", start=i, end=current_square+direction))
                break
        return legal_queen_moves

    def _get_legal_king_moves(self, captures_only:bool):
        legal_king_moves = list()
        for i in range(26,118):
            if self.board[i] == "K":
                # Standard movement
                for direction in KING_DIRECTIONS:
                    if not captures_only and self.board[i+direction] == ' ':
                        sim_board = copy.deepcopy(self)
                        sim_board.move(Move(type="standard", start=i, end=i+direction))
                        if not sim_board.in_check():
                            legal_king_moves.append(Move(type="standard", start=i, end=i+direction))
                    elif self.board[i+direction].islower():
                        sim_board = copy.deepcopy(self)
                        sim_board.move(Move(type="capture", start=i, end=i+direction))
                        if not sim_board.in_check():
                            legal_king_moves.append(Move(type="capture", start=i, end=i+direction))
                # Castling
                if not captures_only and not self.in_check():
                    if self.castle_availablity["queen_side_possible"] and self.castle_availablity["queen_side_clear"]:
                        sim_board = copy.deepcopy(self)
                        sim_board.move(Move(type="castle", castle_side='Q'))
                        if not sim_board.in_check():
                            legal_king_moves.append(Move(type="castle", castle_side='Q'))
                    if self.castle_availablity["king_side_possible"] and self.castle_availablity["king_side_clear"]:
                        sim_board = copy.deepcopy(self)
                        sim_board.move(Move(type="castle", castle_side='K'))
                        if not sim_board.in_check():
                            legal_king_moves.append(Move(type="castle", castle_side='K'))
                    
                break
                
        return legal_king_moves
    
    def in_check(self):
        rotated_board = copy.deepcopy(self)
        rotated_board.rotate_board()
        for pawn_move in rotated_board._get_legal_pawn_moves(captures_only=True):
            if rotated_board.board[pawn_move.end_idx] == 'k':
                return True
        for knight_move in rotated_board._get_legal_knight_moves(captures_only=True):
            if rotated_board.board[knight_move.end_idx] == 'k':
                return True
        for bishop_move in rotated_board._get_legal_bishop_moves(captures_only=True):
            if rotated_board.board[bishop_move.end_idx] == 'k':
                return True
        for rook_move in rotated_board._get_legal_rook_moves(captures_only=True):
            if rotated_board.board[rook_move.end_idx] == 'k':
                return True
        for queen_move in rotated_board._get_legal_queen_moves(captures_only=True):
            if rotated_board.board[queen_move.end_idx] == 'k':
                return True
        return False
    
    def in_checkmate(self) -> bool:
        if self.in_check():
            moves = self.get_legal_moves()
            for move in moves:
                sim_board = copy.deepcopy(self)
                sim_board.move(move)
                if not sim_board.in_check():
                    return False
            return True
        return False
    
    def giving_checkmate(self) -> bool:
        self.rotate_board()
        output = self.in_checkmate()
        self.rotate_board()
        return output

    def in_fifty_move_rule_draw(self) -> bool:
        if self.fifty_move_rule_counter >= 50:
            return True
        else:
            return False
    
    def in_threefold_rep_draw(self) -> bool:
        last_move_idx = len(self.move_stack)-1
        if last_move_idx < 6:
            return False
        if (self.move_stack[last_move_idx] == self.move_stack[last_move_idx-2] == self.move_stack[last_move_idx[-4]]) and (self.move_stack[last_move_idx-1] == self.move_stack[last_move_idx-3] == self.move_stack[last_move_idx[-5]]):
            return True
        else:
            return False

    def game_over(self):
        return self.in_checkmate() or self.giving_checkmate() or self.in_fifty_move_rule_draw() or self.in_threefold_rep_draw()
