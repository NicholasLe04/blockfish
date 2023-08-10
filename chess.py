import pieces.pawn as pawn
import pieces.knight as knight
import pieces.bishop as bishop
import pieces.rook as rook
import pieces.queen as queen
import pieces.king as king

from bitboard_util import set_bit, get_bit, clear_bit, index_of_LSB, index_of_MSB, bitscan
from constants import PIECE_VALUES, POSITION_TO_INDEX, W_KING_CASTLE_CLEAR, W_QUEEN_CASTLE_CLEAR, B_KING_CASTLE_CLEAR, B_QUEEN_CASTLE_CLEAR, ZOBRIST_HASH_TABLE, PIECE_TO_INDEX

class Position():


    def __init__(self):                     
        self.piece_bitboards = {
                                         # Top of board                                            bottom of board
                                    "P": 0x000000000000FF00,  # 00000000_00000000_00000000_00000000_00000000_00000000_11111111_00000000
                                    "N": 0x0000000000000042,  # 00000000_00000000_00000000_00000000_00000000_00000000_00000000_01000010
                                    "B": 0x0000000000000024,  # 00000000_00000000_00000000_00000000_00000000_00000000_00000000_00100100
                                    "R": 0x0000000000000081,  # 00000000_00000000_00000000_00000000_00000000_00000000_00000000_10000001
                                    "Q": 0x0000000000000010,  # 00000000_00000000_00000000_00000000_00000000_00000000_00000000_00010000
                                    "K": 0x0000000000000008,  # 00000000_00000000_00000000_00000000_00000000_00000000_00000000_00001000

                                    "p": 0x00FF000000000000,   # 00000000_11111111_00000000_00000000_00000000_00000000_00000000_00000000
                                    "n": 0x4200000000000000,  # 01000010_00000000_00000000_00000000_00000000_00000000_00000000_00000000
                                    "b": 0x2400000000000000,  # 00100100_00000000_00000000_00000000_00000000_00000000_00000000_00000000
                                    "r": 0x8100000000000000,  # 10000001_00000000_00000000_00000000_00000000_00000000_00000000_00000000
                                    "q": 0x1000000000000000,  # 00010000_00000000_00000000_00000000_00000000_00000000_00000000_00000000
                                    "k": 0x0800000000000000,  # 00001000_00000000_00000000_00000000_00000000_00000000_00000000_00000000
                                }     
        

        self.w_pieces_bb  =  self.piece_bitboards["P"] | self.piece_bitboards["N"] | self.piece_bitboards["B"] | self.piece_bitboards["R"] | self.piece_bitboards["Q"] | self.piece_bitboards["K"]
        self.b_pieces_bb  =  self.piece_bitboards["p"] | self.piece_bitboards["n"] | self.piece_bitboards["b"] | self.piece_bitboards["r"] | self.piece_bitboards["q"] | self.piece_bitboards["k"]

        self.all_pieces_bb = (self.piece_bitboards["P"] | self.piece_bitboards["N"] | self.piece_bitboards["B"] | self.piece_bitboards["R"] | self.piece_bitboards["Q"] | self.piece_bitboards["K"] |
                               self.piece_bitboards["p"] | self.piece_bitboards["n"] | self.piece_bitboards["b"] | self.piece_bitboards["r"] | self.piece_bitboards["q"] | self.piece_bitboards["k"])

        self.white_side = True
        self.castle_availability = { "K": True, "Q": True, "k": True, "q": True }
        self.fifty_rule_counter = 0
        self.en_passant_square = None               
        self.move_stack = []

        self.zobrist_hash = (self.white_side << 68) | (self.compute_castle_bitstring() << 64) | (self.compute_zobrist_hash())

    def compute_zobrist_hash(self):
        hash = 0
        for i in range(64):
            if get_bit(self.all_pieces_bb, i):
                for piece, bitboard in self.piece_bitboards.items():
                    if get_bit(bitboard, i):
                        hash ^= ZOBRIST_HASH_TABLE[i][PIECE_TO_INDEX[piece]]
                        break
        return hash
    
    def compute_castle_bitstring(self):
        return (self.castle_availability["K"] << 3) | (self.castle_availability["Q"] << 2) | (self.castle_availability["k"] << 1) | self.castle_availability["q"]
    
    def print_board(self):
        piece_list = []
        for i in range(63, -1, -1):
            if get_bit(self.piece_bitboards["P"], i):
                piece_list.append('♙')
            elif get_bit(self.piece_bitboards["N"], i):
                piece_list.append('♘')
            elif get_bit(self.piece_bitboards["B"], i):
                piece_list.append('♗')
            elif get_bit(self.piece_bitboards["R"], i):
                piece_list.append('♖')
            elif get_bit(self.piece_bitboards["Q"], i):
                piece_list.append('♕')
            elif get_bit(self.piece_bitboards["K"], i):
                piece_list.append('♔')

            elif get_bit(self.piece_bitboards["p"], i):
                piece_list.append('♟')
            elif get_bit(self.piece_bitboards["n"], i):
                piece_list.append('♞')
            elif get_bit(self.piece_bitboards["b"], i):
                piece_list.append('♝')
            elif get_bit(self.piece_bitboards["r"], i):
                piece_list.append('♜')
            elif get_bit(self.piece_bitboards["q"], i):
                piece_list.append('♛')
            elif get_bit(self.piece_bitboards["k"], i):
                piece_list.append('♚')
            else:
                piece_list.append(' ')

        row = 8
        for i in range(0, 64, 8):
            print("+---+---+---+---+---+---+---+---+")
            print(f"| {piece_list[i]} | {piece_list[i+1]} | {piece_list[i+2]} | {piece_list[i+3]} | {piece_list[i+4]} | {piece_list[i+5]} | {piece_list[i+6]} | {piece_list[i+7]} | {row}")
            row -= 1
        print("+---+---+---+---+---+---+---+---+\n  a   b   c   d   e   f   g   h  ")

    def _update_bitboards(self):
        self.w_pieces_bb = self.piece_bitboards["P"] | self.piece_bitboards["N"] | self.piece_bitboards["B"] | self.piece_bitboards["R"] | self.piece_bitboards["Q"] | self.piece_bitboards["K"]
        self.b_pieces_bb = self.piece_bitboards["p"] | self.piece_bitboards["n"] | self.piece_bitboards["b"] | self.piece_bitboards["r"] | self.piece_bitboards["q"] | self.piece_bitboards["k"]
        self.all_pieces_bb = (self.piece_bitboards["P"] | self.piece_bitboards["N"] | self.piece_bitboards["B"] | self.piece_bitboards["R"] | self.piece_bitboards["Q"] | self.piece_bitboards["K"] |
                               self.piece_bitboards["p"] | self.piece_bitboards["n"] | self.piece_bitboards["b"] | self.piece_bitboards["r"] | self.piece_bitboards["q"] | self.piece_bitboards["k"])

    def _piece_at_index(self, index):
        if get_bit(self.all_pieces_bb, index):
            for piece, bitboard in self.piece_bitboards.items():
                if get_bit(bitboard, index):
                    return piece
        else:
            return ' '

    def from_FEN(self, fen:str):
        pieces, active_side, castling, ep_square, fifty_rule_counter, _ = fen.split(' ')

        # Update Pieces
        self.piece_bitboards["P"], self.piece_bitboards["N"], self.piece_bitboards["B"], self.piece_bitboards["R"], self.piece_bitboards["Q"], self.piece_bitboards["K"] = 0, 0, 0, 0, 0, 0
        self.piece_bitboards["p"], self.piece_bitboards["n"], self.piece_bitboards["b"], self.piece_bitboards["r"], self.piece_bitboards["q"], self.piece_bitboards["k"] = 0, 0, 0, 0, 0, 0

        piece_list = list()
        for i in range(len(pieces)):
            if pieces[i].isalpha():
                piece_list.append(pieces[i])
            elif pieces[i].isdigit():
                empty_squares = list()
                for _ in range(int(pieces[i])):
                    empty_squares.append(' ')
                piece_list += empty_squares
        piece_list.reverse()

        for i in range(64):
            if piece_list[i].isalpha():
                self.piece_bitboards[piece_list[i]] = set_bit(self.piece_bitboards[piece_list[i]], i)

        self._update_bitboards()

        # Update Side
        if active_side == 'w':
            self.white_side = True
        else:
            self.white_side = False

        # Update Castling
        self.castle_availability = { "K": False, "Q": False, "k": False, "q": False }
        if castling != '-':
            for el in castling:
                self.castle_availability[el] = True

        if ep_square != '-':
            ep_idx = POSITION_TO_INDEX[ep_square]
            #set_bit(self.en_passant_square, ep_idx)
            self.en_passant_square = ep_idx

        self.fifty_rule_counter = int(fifty_rule_counter)
        
    def get_attacking_bitboard(self, white=True):
        if white:
            white_attacking_bb = 0
            white_attacking_bb |= pawn.w_pawn_attacks(self.piece_bitboards["P"])

            if self.piece_bitboards["N"]:
                knight_1, knight_2 = index_of_LSB(self.piece_bitboards["N"]), index_of_MSB(self.piece_bitboards["N"])
                white_attacking_bb |= knight.knight_attacks(knight_1)
                if knight_1 != knight_2:
                    white_attacking_bb |= knight.knight_attacks(knight_2)

            if self.piece_bitboards["B"]:
                bishop_1, bishop_2 = index_of_LSB(self.piece_bitboards["B"]), index_of_MSB(self.piece_bitboards["B"])
                white_attacking_bb |= bishop.bishop_attacks(bishop_1, self.all_pieces_bb)
                if bishop_1 != bishop_2:
                    white_attacking_bb |= bishop.bishop_attacks(bishop_2, self.all_pieces_bb)

            if self.piece_bitboards["R"]:
                rook_1, rook_2 = index_of_LSB(self.piece_bitboards["R"]), index_of_MSB(self.piece_bitboards["R"])
                white_attacking_bb |= rook.rook_attacks(rook_1, self.all_pieces_bb)
                if rook_1 != rook_2:
                    white_attacking_bb |= rook.rook_attacks(rook_2, self.all_pieces_bb)

            if self.piece_bitboards["Q"]:
                queen_1 = index_of_LSB(self.piece_bitboards["Q"])
                white_attacking_bb |= queen.queen_attacks(queen_1, self.all_pieces_bb)

            king_1 = index_of_LSB(self.piece_bitboards["K"])
            white_attacking_bb |= king.king_targets(king_1)

            return white_attacking_bb
        else:
            black_attacking_bb = 0
            black_attacking_bb |= pawn.b_pawn_attacks(self.piece_bitboards["p"])

            if self.piece_bitboards["n"]:
                knight_1, knight_2 = index_of_LSB(self.piece_bitboards["n"]), index_of_MSB(self.piece_bitboards["n"])
                black_attacking_bb |= knight.knight_attacks(knight_1)
                if knight_1 != knight_2:
                    black_attacking_bb |= knight.knight_attacks(knight_2)

            if self.piece_bitboards["b"]:
                bishop_1, bishop_2 = index_of_LSB(self.piece_bitboards["b"]), index_of_MSB(self.piece_bitboards["b"])
                black_attacking_bb |= bishop.bishop_attacks(bishop_1, self.all_pieces_bb)
                if bishop_1 != bishop_2:
                    black_attacking_bb |= bishop.bishop_attacks(bishop_2, self.all_pieces_bb)

            if self.piece_bitboards["r"]:
                rook_1, rook_2 = index_of_LSB(self.piece_bitboards["r"]), index_of_MSB(self.piece_bitboards["r"])
                black_attacking_bb |= rook.rook_attacks(rook_1, self.all_pieces_bb)
                if rook_1 != rook_2:
                    black_attacking_bb |= rook.rook_attacks(rook_2, self.all_pieces_bb)

            if self.piece_bitboards["q"]:
                queen_1 = index_of_LSB(self.piece_bitboards["q"])
                black_attacking_bb |= queen.queen_attacks(queen_1, self.all_pieces_bb)

            king_1 = index_of_LSB(self.piece_bitboards["k"])
            black_attacking_bb |= king.king_targets(king_1)

            return black_attacking_bb

    def evaluation(self):
        evalution = 0
        # Pawn material
        evalution += (PIECE_VALUES['P'] * bin(self.piece_bitboards["P"]).count("1"))
        evalution -= (PIECE_VALUES['P'] * bin(self.piece_bitboards["p"]).count("1"))

        # Knight material
        evalution += (PIECE_VALUES['N'] * bin(self.piece_bitboards["N"]).count("1"))
        evalution -= (PIECE_VALUES['N'] * bin(self.piece_bitboards["n"]).count("1"))
        
        # Bishop material
        evalution += (PIECE_VALUES['B'] * bin(self.piece_bitboards["B"]).count("1"))
        evalution -= (PIECE_VALUES['B'] * bin(self.piece_bitboards["b"]).count("1"))
        
        # Rook material
        evalution += (PIECE_VALUES['R'] * bin(self.piece_bitboards["R"]).count("1"))
        evalution -= (PIECE_VALUES['R'] * bin(self.piece_bitboards["r"]).count("1"))
        
        # Queen material
        evalution += PIECE_VALUES['Q'] if self.piece_bitboards["Q"] else 0
        evalution -= PIECE_VALUES['Q'] if self.piece_bitboards["q"] else 0

        return evalution
    
    def get_legal_moves(self, white=True):
        moves = []
        if white:
            for idx in bitscan(self.w_pieces_bb):
                if get_bit(self.w_pieces_bb, idx):
                    move_mask = (1 << idx)
                    # Pawn Move Generation
                    if self.piece_bitboards["P"] & move_mask:
                        row, col = idx // 8, idx % 8  
                        if row < 6:
                            if not get_bit(self.all_pieces_bb, idx + 8):
                                moves.append({"piece": 'P', "start": idx, "end": idx + 8, "code": 0})
                            # Check if the pawn can move two squares forward from its starting position
                            if row == 1 and not get_bit(self.all_pieces_bb, idx + 16) and not get_bit(self.all_pieces_bb, idx + 8):
                                moves.append({"piece": 'P', "start": idx, "end": idx + 16, "code": 1})
                            # Check if the pawn can capture diagonally (left and right)
                            if col > 0 and get_bit(self.b_pieces_bb, idx + 7):
                                moves.append({"piece": 'P', "start": idx, "end": idx + 7, "captured": self._piece_at_index(idx+7), "code": 4})
                            if col < 7 and get_bit(self.b_pieces_bb, idx + 9):
                                moves.append({"piece": 'P', "start": idx, "end": idx + 9, "captured": self._piece_at_index(idx+9), "code": 4})
                            # Check if the pawn can ep capture 
                            if col > 0 and idx + 7 == self.en_passant_square: # get_bit(self.en_passant_square, idx + 7):
                                moves.append({"piece": 'P', "start": idx, "end": idx + 7, "code": 5})
                            if col < 7 and idx + 9 == self.en_passant_square: # and get_bit(self.en_passant_square, idx + 9):
                                moves.append({"piece": 'P', "start": idx, "end": idx + 9, "code": 5})
                        else:  # PROMOTIONS
                            if not get_bit(self.all_pieces_bb, idx + 8):
                                moves.append({"piece": 'P', "start": idx, "end": idx + 8, "code": 8})
                                moves.append({"piece": 'P', "start": idx, "end": idx + 8, "code": 9})
                                moves.append({"piece": 'P', "start": idx, "end": idx + 8, "code": 10})
                                moves.append({"piece": 'P', "start": idx, "end": idx + 8, "code": 11})
                            # Check if the pawn can capture diagonally (left and right)
                            if col > 0 and get_bit(self.b_pieces_bb, idx + 7):
                                moves.append({"piece": 'P', "start": idx, "end": idx + 7, "captured": self._piece_at_index(idx+7), "code": 12})
                                moves.append({"piece": 'P', "start": idx, "end": idx + 7, "captured": self._piece_at_index(idx+7), "code": 13})
                                moves.append({"piece": 'P', "start": idx, "end": idx + 7, "captured": self._piece_at_index(idx+7), "code": 14})
                                moves.append({"piece": 'P', "start": idx, "end": idx + 7, "captured": self._piece_at_index(idx+7), "code": 15})
                            if col < 7 and get_bit(self.b_pieces_bb, idx + 9):
                                moves.append({"piece": 'P', "start": idx, "end": idx + 9, "captured": self._piece_at_index(idx+9), "code": 12})
                                moves.append({"piece": 'P', "start": idx, "end": idx + 9, "captured": self._piece_at_index(idx+9), "code": 13})
                                moves.append({"piece": 'P', "start": idx, "end": idx + 9, "captured": self._piece_at_index(idx+9), "code": 14})
                                moves.append({"piece": 'P', "start": idx, "end": idx + 9, "captured": self._piece_at_index(idx+9), "code": 15})
                    # Knight Move Generation
                    elif self.piece_bitboards["N"] & move_mask:
                        for end_idx in bitscan(knight.knight_moves(idx, self.w_pieces_bb)):
                            if get_bit(self.b_pieces_bb, end_idx):
                                moves.append({"piece": 'N', "start": idx, "end": end_idx, "captured": self._piece_at_index(end_idx), "code": 4})
                            else:
                                moves.append({"piece": 'N', "start": idx, "end": end_idx, "code": 0})
                    # Bishop Move Generation
                    elif self.piece_bitboards["B"] & move_mask:
                        for end_idx in bitscan(bishop.bishop_moves(idx, self.w_pieces_bb, self.all_pieces_bb)):
                            if get_bit(self.b_pieces_bb, end_idx):
                                moves.append({"piece": 'B', "start": idx, "end": end_idx, "captured": self._piece_at_index(end_idx), "code": 4})
                            else:
                                moves.append({"piece": 'B', "start": idx, "end": end_idx, "code": 0})
                    # Rook Move Generation
                    elif self.piece_bitboards["R"] & move_mask:
                        for end_idx in bitscan(rook.rook_moves(idx, self.w_pieces_bb, self.all_pieces_bb)):
                            if get_bit(self.b_pieces_bb, end_idx):
                                moves.append({"piece": 'R', "start": idx, "end": end_idx, "captured": self._piece_at_index(end_idx), "code": 4})
                            else:
                                moves.append({"piece": 'R', "start": idx, "end": end_idx, "code": 0})
                    # Queen Move Generation
                    elif self.piece_bitboards["Q"] & move_mask:
                        for end_idx in bitscan(queen.queen_moves(idx, self.w_pieces_bb, self.all_pieces_bb)):
                            if get_bit(self.b_pieces_bb, end_idx):
                                moves.append({"piece": 'Q', "start": idx, "end": end_idx, "captured": self._piece_at_index(end_idx), "code": 4})
                            else:
                                moves.append({"piece": 'Q', "start": idx, "end": end_idx, "code": 0})
                    # King Move Generation
                    elif self.piece_bitboards["K"] & move_mask:
                        for end_idx in bitscan(king.king_moves(idx, self.w_pieces_bb)):
                            # Quiet moves and captures
                            if get_bit(self.b_pieces_bb, end_idx):
                                moves.append({"piece": 'K', "start": idx, "end": end_idx, "captured": self._piece_at_index(end_idx), "code": 4})
                            else:
                                moves.append({"piece": 'K', "start": idx, "end": end_idx, "code": 0})
                            # Castle
                        if self.castle_availability['K'] and not (W_KING_CASTLE_CLEAR & self.all_pieces_bb) and (get_bit(self.piece_bitboards["R"], 0)):
                            moves.append({"piece": 'K', "code": 2})
                        if self.castle_availability['Q'] and not (W_QUEEN_CASTLE_CLEAR & self.all_pieces_bb) and (get_bit(self.piece_bitboards["R"], 7)):
                            moves.append({"piece": 'K', "code": 3})

        else:
            for idx in bitscan(self.b_pieces_bb):
                if get_bit(self.b_pieces_bb, idx):
                    move_mask = (1 << idx)
                    # Pawn Move Generation
                    if self.piece_bitboards["p"] & move_mask:
                        row, col = idx // 8, idx % 8  
                        if row > 1:
                            if not get_bit(self.all_pieces_bb, idx - 8):
                                moves.append({"piece": 'p', "start": idx, "end": idx - 8, "code": 0})
                            # Check if the pawn can move two squares forward from its starting position
                            if row == 6 and not get_bit(self.all_pieces_bb, idx - 16) and not get_bit(self.all_pieces_bb, idx - 8):
                                moves.append({"piece": 'p', "start": idx, "end": idx - 16, "code": 1})
                            # Check if the pawn can capture diagonally (left and right)
                            if col < 7 and get_bit(self.w_pieces_bb, idx - 7):
                                moves.append({"piece": 'p', "start": idx, "end": idx - 7, "captured": self._piece_at_index(idx - 7), "code": 4})
                            if col > 0 and get_bit(self.w_pieces_bb, idx - 9):
                                moves.append({"piece": 'p', "start": idx, "end": idx - 9, "captured": self._piece_at_index(idx - 9), "code": 4})
                            # Check if the pawn can ep capture 
                            if col < 7 and idx - 7 == self.en_passant_square: # and get_bit(self.en_passant_square, idx - 7):
                                moves.append({"piece": 'p', "start": idx, "end": idx - 7, "code": 5})
                            if col > 0 and idx - 9 == self.en_passant_square: # and get_bit(self.en_passant_square, idx - 9):
                                moves.append({"piece": 'p', "start": idx, "end": idx - 9, "code": 5})
                        else:  # PROMOTIONS
                            if not get_bit(self.all_pieces_bb, idx - 8):
                                moves.append({"piece": 'p', "start": idx, "end": idx - 8, "code": 8})
                                moves.append({"piece": 'p', "start": idx, "end": idx - 8, "code": 9})
                                moves.append({"piece": 'p', "start": idx, "end": idx - 8, "code": 10})
                                moves.append({"piece": 'p', "start": idx, "end": idx - 8, "code": 11})
                            # Check if the pawn can capture diagonally (left and right)
                            if col < 7 and get_bit(self.b_pieces_bb, idx - 7):
                                moves.append({"piece": 'p', "start": idx, "end": idx - 7, "captured": self._piece_at_index(idx - 7), "code": 12})
                                moves.append({"piece": 'p', "start": idx, "end": idx - 7, "captured": self._piece_at_index(idx - 7), "code": 13})
                                moves.append({"piece": 'p', "start": idx, "end": idx - 7, "captured": self._piece_at_index(idx - 7), "code": 14})
                                moves.append({"piece": 'p', "start": idx, "end": idx - 7, "captured": self._piece_at_index(idx - 7), "code": 15})
                            if col > 0 and get_bit(self.b_pieces_bb, idx - 9):
                                moves.append({"piece": 'p', "start": idx, "end": idx - 9, "captured": self._piece_at_index(idx - 9), "code": 12})
                                moves.append({"piece": 'p', "start": idx, "end": idx - 9, "captured": self._piece_at_index(idx - 9), "code": 13})
                                moves.append({"piece": 'p', "start": idx, "end": idx - 9, "captured": self._piece_at_index(idx - 9), "code": 14})
                                moves.append({"piece": 'p', "start": idx, "end": idx - 9, "captured": self._piece_at_index(idx - 9), "code": 15})
                    # Knight Move Generation
                    elif self.piece_bitboards["n"] & move_mask:
                        for end_idx in bitscan(knight.knight_moves(idx, self.b_pieces_bb)):
                            if get_bit(self.w_pieces_bb, end_idx):
                                moves.append({"piece": 'n', "start": idx, "end": end_idx, "captured": self._piece_at_index(end_idx), "code": 4})
                            else:
                                moves.append({"piece": 'n', "start": idx, "end": end_idx, "code": 0})
                    # Bishop Move Generation
                    elif self.piece_bitboards["b"] & move_mask:
                        for end_idx in bitscan(bishop.bishop_moves(idx, self.b_pieces_bb, self.all_pieces_bb)):
                            if get_bit(self.w_pieces_bb, end_idx):
                                moves.append({"piece": 'b', "start": idx, "end": end_idx, "captured": self._piece_at_index(end_idx), "code": 4})
                            else:
                                moves.append({"piece": 'b', "start": idx, "end": end_idx, "code": 0})            
                    # Rook Move Generation
                    elif self.piece_bitboards["r"] & move_mask:
                        for end_idx in bitscan(rook.rook_moves(idx, self.b_pieces_bb, self.all_pieces_bb)):
                            if get_bit(self.w_pieces_bb, end_idx):
                                moves.append({"piece": 'r', "start": idx, "end": end_idx, "captured": self._piece_at_index(end_idx), "code": 4})
                            else:
                                moves.append({"piece": 'r', "start": idx, "end": end_idx, "code": 0})
                    # Queen Move Generation
                    elif self.piece_bitboards["q"] & move_mask:
                        for end_idx in bitscan(queen.queen_moves(idx, self.b_pieces_bb, self.all_pieces_bb)):
                            if get_bit(self.w_pieces_bb, end_idx):
                                moves.append({"piece": 'q', "start": idx, "end": end_idx, "captured": self._piece_at_index(end_idx), "code": 4})
                            else:
                                moves.append({"piece": 'q', "start": idx, "end": end_idx, "code": 0})
                    # King Move Generation
                    elif self.piece_bitboards["k"] & move_mask:
                        for end_idx in bitscan(king.king_moves(idx, self.b_pieces_bb)):
                            # Quiet moves and captures
                            if get_bit(self.w_pieces_bb, end_idx):
                                moves.append({"piece": 'k', "start": idx, "end": end_idx, "captured": self._piece_at_index(end_idx), "code": 4})
                            else:
                                moves.append({"piece": 'k', "start": idx, "end": end_idx, "code": 0})
                        # Castle
                        if self.castle_availability['k'] and not (B_KING_CASTLE_CLEAR & self.all_pieces_bb) and (get_bit(self.piece_bitboards["r"], 56)):
                            moves.append({"piece": 'k', "code": 2})
                        if self.castle_availability['q'] and not (B_QUEEN_CASTLE_CLEAR & self.all_pieces_bb) and (get_bit(self.piece_bitboards["r"], 63)):
                            moves.append({"piece": 'k', "code": 3})
        
        # Ensure king not in check after move
        legal_moves = []
        captures = { "p":[], "n":[], "b":[], "r":[], "q":[], "k":[], }
        for move in moves:
            if not((move["code"] == 4 or 12 <= move["code"] <= 15) and move["captured"].lower() == 'k'):
                hash = self.zobrist_hash
                self.make_move(move)
                if not self.in_check(white):
                    # Order moves with captures first
                    if move["code"] == 4 or 12 <= move["code"] <= 15:
                        captures[move["piece"].lower()].append(move)
                        #legal_moves.insert(0, move)
                    else:
                        legal_moves.append(move)
                self.unmake_move(move, hash)
        
        return captures["p"] + captures["n"] + captures["b"] + captures["r"] + captures["q"] + captures["k"] + legal_moves
        #return legal_moves

    def in_check(self, white=True) -> bool:
        if white:
            return bool(self.piece_bitboards["K"] & self.get_attacking_bitboard(False))
        else:
            return bool(self.piece_bitboards["k"] & self.get_attacking_bitboard(True))

    def in_checkmate(self, white=True) -> bool:
        if self.in_check() and len(self.get_legal_moves()) == 0:
            return True
        return False

    def in_fifty_move_rule_draw(self) -> bool:
        if self.fifty_rule_counter >= 50:
            return True
        return False
    
    def in_threefold_rep_draw(self) -> bool:
        last_move_idx = len(self.move_stack)-1
        if last_move_idx < 6:
            return False
        if (self.move_stack[last_move_idx] == self.move_stack[last_move_idx-4]) and (self.move_stack[last_move_idx-1] == self.move_stack[last_move_idx-5]):
            return True
        else:
            return False
    

    def in_game_over(self):
        return self.in_checkmate() or self.in_checkmate(False) or self.in_fifty_move_rule_draw() or self.in_threefold_rep_draw()

    def make_move(self, move:dict):
        '''Give a move in dictionary format (i.e. {"piece": 'P', "start": 8, "end": 16, "code": 0})'''

        # Reset en passant
        self.en_passant_square = None
        self.zobrist_hash &= 0xF_FF_FF_FF_FF_FF_FF_FF_FF    # 11111100_00001111_11111111_11111111_11111111_11111111_11111111_11111111_11111111_11111111

        # Update side
        self.white_side = not self.white_side
        self.zobrist_hash ^= (1 << 68)

        match move["code"]:

            case 0 | 4: # Quiet Moves and Captures

                moved_piece = move["piece"]

                self.piece_bitboards[moved_piece] = clear_bit(self.piece_bitboards[moved_piece], move["start"])
                self.piece_bitboards[moved_piece] = set_bit(self.piece_bitboards[moved_piece], move["end"])
                self.zobrist_hash ^= ZOBRIST_HASH_TABLE[move["start"]][PIECE_TO_INDEX[moved_piece]]
                self.zobrist_hash ^= ZOBRIST_HASH_TABLE[move["end"]][PIECE_TO_INDEX[moved_piece]]
                    
                if move["code"] == 4:
                    captured_piece = move["captured"]
                    self.piece_bitboards[captured_piece] = clear_bit(self.piece_bitboards[captured_piece], move["end"])
                    self.zobrist_hash ^= ZOBRIST_HASH_TABLE[move["end"]][PIECE_TO_INDEX[captured_piece]]

            case 1: # Double Pawn Push
                if move["piece"] == 'P':
                    self.piece_bitboards["P"] = clear_bit(self.piece_bitboards["P"], move["start"])
                    self.piece_bitboards["P"] = set_bit(self.piece_bitboards["P"], move["end"])
                    self.zobrist_hash ^= ZOBRIST_HASH_TABLE[move["start"]][0]
                    self.zobrist_hash ^= ZOBRIST_HASH_TABLE[move["end"]][0]
                    self.en_passant_square = move["start"] + 8
                else:
                    self.piece_bitboards["p"] = clear_bit(self.piece_bitboards["p"], move["start"])
                    self.piece_bitboards["p"] = set_bit(self.piece_bitboards["p"], move["end"])
                    self.zobrist_hash ^= ZOBRIST_HASH_TABLE[move["start"]][6]
                    self.zobrist_hash ^= ZOBRIST_HASH_TABLE[move["end"]][6]
                    self.en_passant_square = move["start"] - 8
                self.zobrist_hash |= (self.en_passant_square << 69)

            case 2: # King Side Castle
                if move["piece"].isupper(): # White
                    self.piece_bitboards["K"] = self.piece_bitboards["K"] >> 2
                    self.piece_bitboards["R"] = clear_bit(self.piece_bitboards["R"], 0)
                    self.piece_bitboards["R"] = set_bit(self.piece_bitboards["R"], 2)
                    self.zobrist_hash ^= ZOBRIST_HASH_TABLE[0][3]
                    self.zobrist_hash ^= ZOBRIST_HASH_TABLE[2][3]
                    self.zobrist_hash ^= ZOBRIST_HASH_TABLE[3][5]
                    self.zobrist_hash ^= ZOBRIST_HASH_TABLE[1][5]
                    self.zobrist_hash &= ~(1 << 67)
                else:                       # Black
                    self.piece_bitboards["k"] = self.piece_bitboards["k"] >> 2
                    self.piece_bitboards["r"] = clear_bit(self.piece_bitboards["r"], 56)
                    self.piece_bitboards["r"] = set_bit(self.piece_bitboards["r"], 58)
                    self.zobrist_hash ^= ZOBRIST_HASH_TABLE[56][9]
                    self.zobrist_hash ^= ZOBRIST_HASH_TABLE[58][9]
                    self.zobrist_hash ^= ZOBRIST_HASH_TABLE[59][11]
                    self.zobrist_hash ^= ZOBRIST_HASH_TABLE[57][11]
                    self.zobrist_hash &= ~(1 << 65)

            case 3: # Queen Side Castle
                if move["piece"].isupper(): # White
                    self.piece_bitboards["K"] = self.piece_bitboards["K"] << 2
                    self.piece_bitboards["R"] = clear_bit(self.piece_bitboards["R"], 7)
                    self.piece_bitboards["R"] = set_bit(self.piece_bitboards["R"], 4)
                    self.zobrist_hash ^= ZOBRIST_HASH_TABLE[7][3]
                    self.zobrist_hash ^= ZOBRIST_HASH_TABLE[4][3]
                    self.zobrist_hash ^= ZOBRIST_HASH_TABLE[3][5]
                    self.zobrist_hash ^= ZOBRIST_HASH_TABLE[5][5]
                    self.zobrist_hash &= ~(1 << 66)
                else:                       # Black
                    self.piece_bitboards["k"] = self.piece_bitboards["k"] << 2
                    self.piece_bitboards["r"] = clear_bit(self.piece_bitboards["r"], 63)
                    self.piece_bitboards["r"] = set_bit(self.piece_bitboards["r"], 60)
                    self.zobrist_hash ^= ZOBRIST_HASH_TABLE[63][9]
                    self.zobrist_hash ^= ZOBRIST_HASH_TABLE[60][9]
                    self.zobrist_hash ^= ZOBRIST_HASH_TABLE[59][11]
                    self.zobrist_hash ^= ZOBRIST_HASH_TABLE[61][11]
                    self.zobrist_hash &= ~(1 << 64)
        
            case 5: # En Passant Capture
                if move["piece"] == 'P':
                    self.piece_bitboards["P"] = clear_bit(self.piece_bitboards["P"], move["start"])
                    self.piece_bitboards["p"] = clear_bit(self.piece_bitboards["p"], move["end"]-8)
                    self.piece_bitboards["P"] = set_bit(self.piece_bitboards["P"], move["end"])
                    self.zobrist_hash ^= ZOBRIST_HASH_TABLE[move["start"]][0]
                    self.zobrist_hash ^= ZOBRIST_HASH_TABLE[move["end"]][0]
                    self.zobrist_hash ^= ZOBRIST_HASH_TABLE[move["end"]-8][6]
                else:
                    self.piece_bitboards["p"] = clear_bit(self.piece_bitboards["p"], move["start"])
                    self.piece_bitboards["P"] = clear_bit(self.piece_bitboards["P"], move["end"]+8)
                    self.piece_bitboards["p"] = set_bit(self.piece_bitboards["p"], move["end"])
                    self.zobrist_hash ^= ZOBRIST_HASH_TABLE[move["start"]][6]
                    self.zobrist_hash ^= ZOBRIST_HASH_TABLE[move["end"]][6]
                    self.zobrist_hash ^= ZOBRIST_HASH_TABLE[move["end"]+8][0]

            case 8: # Quiet Knight Promotion
                if move["piece"] == 'P':
                    self.piece_bitboards["P"] = clear_bit(self.piece_bitboards["P"], move["start"])
                    self.piece_bitboards["N"] = set_bit(self.piece_bitboards["N"], move["end"])
                    self.zobrist_hash ^= ZOBRIST_HASH_TABLE[move["start"]][0]
                    self.zobrist_hash ^= ZOBRIST_HASH_TABLE[move["end"]][1]
                else:
                    self.piece_bitboards["p"] = clear_bit(self.piece_bitboards["p"], move["start"])
                    self.piece_bitboards["n"] = set_bit(self.piece_bitboards["n"], move["end"])
                    self.zobrist_hash ^= ZOBRIST_HASH_TABLE[move["start"]][6]
                    self.zobrist_hash ^= ZOBRIST_HASH_TABLE[move["end"]][7]

            case 9: # Quiet Bishop Promotion
                if move["piece"] == 'P':
                    self.piece_bitboards["P"] = clear_bit(self.piece_bitboards["P"], move["start"])
                    self.piece_bitboards["B"] = set_bit(self.piece_bitboards["B"], move["end"])
                    self.zobrist_hash ^= ZOBRIST_HASH_TABLE[move["start"]][0]
                    self.zobrist_hash ^= ZOBRIST_HASH_TABLE[move["end"]][2]
                else:
                    self.piece_bitboards["p"] = clear_bit(self.piece_bitboards["p"], move["start"])
                    self.piece_bitboards["b"] = set_bit(self.piece_bitboards["b"], move["end"])
                    self.zobrist_hash ^= ZOBRIST_HASH_TABLE[move["start"]][6]
                    self.zobrist_hash ^= ZOBRIST_HASH_TABLE[move["end"]][8]

            case 10: # Quiet Rook Promotion
                if move["piece"] == 'P':
                    self.piece_bitboards["P"] = clear_bit(self.piece_bitboards["P"], move["start"])
                    self.piece_bitboards["R"] = set_bit(self.piece_bitboards["R"], move["end"])
                    self.zobrist_hash ^= ZOBRIST_HASH_TABLE[move["start"]][0]
                    self.zobrist_hash ^= ZOBRIST_HASH_TABLE[move["end"]][3]
                else:
                    self.piece_bitboards["p"] = clear_bit(self.piece_bitboards["p"], move["start"])
                    self.piece_bitboards["r"] = set_bit(self.piece_bitboards["r"], move["end"])
                    self.zobrist_hash ^= ZOBRIST_HASH_TABLE[move["start"]][6]
                    self.zobrist_hash ^= ZOBRIST_HASH_TABLE[move["end"]][9]

            case 11: # Quiet Queen Promotion:
                if move["piece"] == 'P':
                    self.piece_bitboards["P"] = clear_bit(self.piece_bitboards["P"], move["start"])
                    self.piece_bitboards["Q"] = set_bit(self.piece_bitboards["Q"], move["end"])
                    self.zobrist_hash ^= ZOBRIST_HASH_TABLE[move["start"]][0]
                    self.zobrist_hash ^= ZOBRIST_HASH_TABLE[move["end"]][4]
                else:
                    self.piece_bitboards["p"] = clear_bit(self.piece_bitboards["p"], move["start"])
                    self.piece_bitboards["q"] = set_bit(self.piece_bitboards["q"], move["end"])
                    self.zobrist_hash ^= ZOBRIST_HASH_TABLE[move["start"]][6]
                    self.zobrist_hash ^= ZOBRIST_HASH_TABLE[move["end"]][10]

            case 12 | 13 | 14 | 15: # Capture Promotion
                captured_piece = move["captured"]
                self.piece_bitboards[captured_piece] = clear_bit(self.piece_bitboards[captured_piece], move["end"])
                self.zobrist_hash ^= ZOBRIST_HASH_TABLE[move["end"]][PIECE_TO_INDEX[captured_piece]]

                if move["piece"] == 'P':
                    self.piece_bitboards["P"] = clear_bit(self.piece_bitboards["P"], move["start"])
                    self.zobrist_hash ^= ZOBRIST_HASH_TABLE[move["start"]][0]

                    if move["code"] == 12:
                        self.piece_bitboards["N"] = set_bit(self.piece_bitboards["N"], move["end"])
                        self.zobrist_hash ^= ZOBRIST_HASH_TABLE[move["end"]][1]
                    elif move["code"] == 13:
                        self.piece_bitboards["B"] = set_bit(self.piece_bitboards["B"], move["end"])
                        self.zobrist_hash ^= ZOBRIST_HASH_TABLE[move["end"]][2]
                    elif move["code"] == 14:
                        self.piece_bitboards["R"] = set_bit(self.piece_bitboards["R"], move["end"])
                        self.zobrist_hash ^= ZOBRIST_HASH_TABLE[move["end"]][3]
                    elif move["code"] == 15:
                        self.piece_bitboards["Q"] = set_bit(self.piece_bitboards["Q"], move["end"])
                        self.zobrist_hash ^= ZOBRIST_HASH_TABLE[move["end"]][4]
                    
                else: 
                    self.piece_bitboards["p"] = clear_bit(self.piece_bitboards["p"], move["start"])
                    self.zobrist_hash ^= ZOBRIST_HASH_TABLE[move["start"]][6]

                    if move["code"] == 12:
                        self.piece_bitboards["n"] = set_bit(self.piece_bitboards["n"], move["end"])
                        self.zobrist_hash ^= ZOBRIST_HASH_TABLE[move["end"]][7]
                    elif move["code"] == 13:
                        self.piece_bitboards["b"] = set_bit(self.piece_bitboards["b"], move["end"])
                        self.zobrist_hash ^= ZOBRIST_HASH_TABLE[move["end"]][8]
                    elif move["code"] == 14:
                        self.piece_bitboards["r"] = set_bit(self.piece_bitboards["r"], move["end"])
                        self.zobrist_hash ^= ZOBRIST_HASH_TABLE[move["end"]][9]
                    elif move["code"] == 15:
                        self.piece_bitboards["q"] = set_bit(self.piece_bitboards["q"], move["end"])
                        self.zobrist_hash ^= ZOBRIST_HASH_TABLE[move["end"]][10]


            case _:
                print("invalid code brotha")
        
        
        # Update Fifty move rule counter
        if move["piece"].lower() != 'p' and move["code"] != 4:
            self.fifty_rule_counter += 1
        else:
            self.fifty_rule_counter = 0

        self.move_stack.append(move)
        
        self._update_bitboards()

    def unmake_move(self, move:dict, previous_zobrist_hash):
        self.zobrist_hash = previous_zobrist_hash

        # Undo en passant
        self.en_passant_square = previous_zobrist_hash & ~(0xF_FF_FF_FF_FF_FF_FF_FF_FF)

        # Undo Castle Availability
        self.castle_availability = { 
                                        "K": bool(get_bit(previous_zobrist_hash,67)), 
                                        "Q": bool(get_bit(previous_zobrist_hash,66)), 
                                        "k": bool(get_bit(previous_zobrist_hash,65)), 
                                        "q": bool(get_bit(previous_zobrist_hash,64)) 
                                   }

        # Undo side
        self.white_side = not self.white_side

        # LEFT OFF HERE GANG
        match move["code"]:

            case 0 | 4: # Quiet Moves and Captures
                
                moved_piece = move["piece"]
                self.piece_bitboards[moved_piece] = set_bit(self.piece_bitboards[moved_piece], move["start"])
                self.piece_bitboards[moved_piece] = clear_bit(self.piece_bitboards[moved_piece], move["end"])

                if move["code"] == 4:
                    captured_piece = move["captured"]
                    self.piece_bitboards[captured_piece] = set_bit(self.piece_bitboards[captured_piece], move["end"])

            case 1: # Double Pawn Push
                if move["piece"] == 'P':
                    self.piece_bitboards["P"] = set_bit(self.piece_bitboards["P"], move["start"])
                    self.piece_bitboards["P"] = clear_bit(self.piece_bitboards["P"], move["end"])
                else:
                    self.piece_bitboards["p"] = set_bit(self.piece_bitboards["p"], move["start"])
                    self.piece_bitboards["p"] = clear_bit(self.piece_bitboards["p"], move["end"])
            
            case 2: # King Side Castle
                if move["piece"].isupper(): # White
                    self.piece_bitboards["K"] = self.piece_bitboards["K"] << 2
                    self.piece_bitboards["R"] = set_bit(self.piece_bitboards["R"], 0)
                    self.piece_bitboards["R"] = clear_bit(self.piece_bitboards["R"], 2)
                else:                       # Black
                    self.piece_bitboards["k"] = self.piece_bitboards["k"] << 2
                    self.piece_bitboards["r"] = set_bit(self.piece_bitboards["r"], 56)
                    self.piece_bitboards["r"] = clear_bit(self.piece_bitboards["r"], 58)

            case 3: # Queen Side Castle
                if move["piece"].isupper(): # White
                    self.piece_bitboards["K"] = self.piece_bitboards["K"] >> 2
                    self.piece_bitboards["R"] = set_bit(self.piece_bitboards["R"], 7)
                    self.piece_bitboards["R"] = clear_bit(self.piece_bitboards["R"], 4)
                else:                       # Black
                    self.piece_bitboards["k"] = self.piece_bitboards["k"] >> 2
                    self.piece_bitboards["r"] = set_bit(self.piece_bitboards["r"], 63)
                    self.piece_bitboards["r"] = clear_bit(self.piece_bitboards["r"], 60)

            case 5: # En Passant Capture
                if move["piece"] == 'P':
                    self.piece_bitboards["P"] = set_bit(self.piece_bitboards["P"], move["start"])
                    self.piece_bitboards["p"] = set_bit(self.piece_bitboards["p"], move["end"]-8)
                    self.piece_bitboards["P"] = clear_bit(self.piece_bitboards["P"], move["end"])
                else:
                    self.piece_bitboards["p"] = set_bit(self.piece_bitboards["p"], move["start"])
                    self.piece_bitboards["P"] = set_bit(self.piece_bitboards["P"], move["end"]+8)
                    self.piece_bitboards["p"] = clear_bit(self.piece_bitboards["p"], move["end"])

            case 8: # Quiet Knight Promotion
                if move["piece"] == 'P':
                    self.piece_bitboards["P"] = set_bit(self.piece_bitboards["P"], move["start"])
                    self.piece_bitboards["N"] = clear_bit(self.piece_bitboards["N"], move["end"])
                else:
                    self.piece_bitboards["p"] = set_bit(self.piece_bitboards["p"], move["start"])
                    self.piece_bitboards["n"] = clear_bit(self.piece_bitboards["n"], move["end"])

            case 9: # Quiet Bishop Promotion
                if move["piece"] == 'P':
                    self.piece_bitboards["P"] = set_bit(self.piece_bitboards["P"], move["start"])
                    self.piece_bitboards["B"] = clear_bit(self.piece_bitboards["B"], move["end"])
                else:
                    self.piece_bitboards["p"] = set_bit(self.piece_bitboards["p"], move["start"])
                    self.piece_bitboards["b"] = clear_bit(self.piece_bitboards["b"], move["end"])

            case 10: # Quiet Rook Promotion
                if move["piece"] == 'P':
                    self.piece_bitboards["P"] =set_bit(self.piece_bitboards["P"], move["start"])
                    self.piece_bitboards["R"] =  clear_bit(self.piece_bitboards["R"], move["end"])
                else:
                    self.piece_bitboards["p"] =set_bit(self.piece_bitboards["p"], move["start"])
                    self.piece_bitboards["r"] =  clear_bit(self.piece_bitboards["r"], move["end"])

            case 11: # Quiet Queen Promotion:
                if move["piece"] == 'P':
                    self.piece_bitboards["P"] = set_bit(self.piece_bitboards["P"], move["start"])
                    self.piece_bitboards["Q"] = clear_bit(self.piece_bitboards["Q"], move["end"])
                else:
                    self.piece_bitboards["p"] = set_bit(self.piece_bitboards["p"], move["start"])
                    self.piece_bitboards["q"] = clear_bit(self.piece_bitboards["q"], move["end"])
            
            case 12 | 13 | 14 | 15: # Capture Promotion
                captured_piece = move["captured"]
                self.piece_bitboards[captured_piece] = set_bit(self.piece_bitboards[captured_piece], move["end"])
                if move["piece"] == 'P':

                    self.piece_bitboards["P"] = set_bit(self.piece_bitboards["P"], move["start"])
                    if move["code"] == 12:
                        self.piece_bitboards["N"] = clear_bit(self.piece_bitboards["N"], move["end"])
    
                    elif move["code"] == 13:
                        self.piece_bitboards["B"] = clear_bit(self.piece_bitboards["B"], move["end"])
    
                    elif move["code"] == 14:
                        self.piece_bitboards["R"] = clear_bit(self.piece_bitboards["R"], move["end"])
    
                    elif move["code"] == 15:
                        self.piece_bitboards["Q"] = clear_bit(self.piece_bitboards["Q"], move["end"])
                    
                else: 
                    self.piece_bitboards["p"] = set_bit(self.piece_bitboards["p"], move["start"])

                    if move["code"] == 12:
                        self.piece_bitboards["n"] = clear_bit(self.piece_bitboards["n"], move["end"])
    
                    elif move["code"] == 13:
                        self.piece_bitboards["b"] = clear_bit(self.piece_bitboards["b"], move["end"])
    
                    elif move["code"] == 14:
                        self.piece_bitboards["r"] = clear_bit(self.piece_bitboards["r"], move["end"])
    
                    elif move["code"] == 15:
                        self.piece_bitboards["q"] = clear_bit(self.piece_bitboards["q"], move["end"])

            case _:
                print("invalid code brotha")

        self.move_stack.pop()
        
        self._update_bitboards()