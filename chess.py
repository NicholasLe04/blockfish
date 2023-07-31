import pieces.pawn as pawn
import pieces.knight as knight
import pieces.bishop as bishop
import pieces.rook as rook
import pieces.queen as queen
import pieces.king as king

from bitboard_util import get_bit, bitboard_to_board, index_of_MSB, index_of_LSB, bitscan

import constants
import time

KNIGHT_DIRECTIONS = [ -25, -23, -10, 14, 25, 23, 10, -14 ]
BISHOP_DIRECTIONS = [ -13, -11, 11, 13 ]
ROOK_DIRECTIONS = [ -1, -12, 1, 12 ]
QUEEN_DIRECTIONS = ROOK_DIRECTIONS + BISHOP_DIRECTIONS
KING_DIRECTIONS = ROOK_DIRECTIONS + BISHOP_DIRECTIONS

PIECE_VALUES = { 
                'P': 1, 'N': 3.05, 'B': 3.33, 'R': 5.63, 'Q': 9.5, 'K': 0 , 
                } # Per AlphaZero


class Position():


    def __init__(self):      # Top of board                                                   bottom of board
        self.w_pawn_bb =     int("00000000_00000000_00000000_00000000_00000000_00000000_11111111_00000000", 2)
        self.w_knight_bb =   int("00000000_00000000_00000000_00000000_00000000_00000000_00000000_01000010", 2)
        self.w_bishop_bb =   int("00000000_00000000_00000000_00000000_00000000_00000000_00000000_00100100", 2)
        self.w_rook_bb =     int("00000000_00000000_00000000_00000000_00000000_00000000_00000000_10000001", 2)
        self.w_queen_bb =    int("00000000_00000000_00000000_00000000_00000000_00000000_00000000_00010000", 2)
        self.w_king_bb =     int("00000000_00000000_00000000_00000000_00000000_00000000_00000000_00001000", 2)
        self.w_pieces_bb = self.w_pawn_bb | self.w_knight_bb | self.w_bishop_bb | self.w_rook_bb | self.w_queen_bb | self.w_king_bb

        self.b_pawn_bb =     int("00000000_11111111_00000000_00000000_00000000_00000000_00000000_00000000", 2)
        self.b_knight_bb =   int("01000010_00000000_00000000_00000000_00000000_00000000_00000000_00000000", 2)
        self.b_bishop_bb =   int("00100100_00000000_00000000_00000000_00000000_00000000_00000000_00000000", 2)
        self.b_rook_bb =     int("10000001_00000000_00000000_00000000_00000000_00000000_00000000_00000000", 2)
        self.b_queen_bb =    int("00010000_00000000_00000000_00000000_00000000_00000000_00000000_00000000", 2)
        self.b_king_bb =     int("00001000_00000000_00000000_00000000_00000000_00000000_00000000_00000000", 2)
        self.b_pieces_bb = self.b_pawn_bb | self.b_knight_bb | self.b_bishop_bb | self.b_rook_bb | self.b_queen_bb | self.b_king_bb

        self.all_pieces_bb = (self.w_pawn_bb | self.w_knight_bb | self.w_bishop_bb | self.w_rook_bb | self.w_queen_bb | self.w_king_bb |
                               self.b_pawn_bb | self.b_knight_bb | self.b_bishop_bb | self.b_rook_bb | self.b_queen_bb | self.b_king_bb)

        self.castle_availability = { "K": True, "Q": True, "k": True, "q": True }
        self.en_passant_square = int("00000000_00000000_00000000_00000000_00000000_00000000_00000000_00000000", 2)

    def get_attacking_bitboard(self, white=True):
        if white:
            white_attacking_bb = 0
            white_attacking_bb |= pawn.w_pawn_attacks(self.w_pawn_bb)

            knight_1, knight_2 = index_of_LSB(self.w_knight_bb), index_of_MSB(self.w_knight_bb)
            white_attacking_bb |= knight.knight_attacks(knight_1)
            white_attacking_bb |= knight.knight_attacks(knight_2)

            bishop_1, bishop_2 = index_of_LSB(self.w_bishop_bb), index_of_MSB(self.w_bishop_bb)
            white_attacking_bb |= bishop.bishop_attacks(bishop_1, self.all_pieces_bb)
            white_attacking_bb |= bishop.bishop_attacks(bishop_2, self.all_pieces_bb)

            rook_1, rook_2 = index_of_LSB(self.w_rook_bb), index_of_MSB(self.w_rook_bb)
            white_attacking_bb |= rook.rook_attacks(rook_1, self.all_pieces_bb)
            white_attacking_bb |= rook.rook_attacks(rook_2, self.all_pieces_bb)

            queen_1 = index_of_LSB(self.w_queen_bb)
            white_attacking_bb |= queen.queen_attacks(queen_1, self.all_pieces_bb)

            king_1 = index_of_LSB(self.w_king_bb)
            white_attacking_bb |= king.king_targets(king_1)

            return white_attacking_bb
        else:
            black_attacking_bb = 0
            black_attacking_bb |= pawn.b_pawn_attacks(self.b_pawn_bb)

            knight_1, knight_2 = index_of_LSB(self.b_knight_bb), index_of_MSB(self.b_knight_bb)
            black_attacking_bb |= knight.knight_attacks(knight_1)
            black_attacking_bb |= knight.knight_attacks(knight_2)

            bishop_1, bishop_2 = index_of_LSB(self.b_bishop_bb), index_of_MSB(self.b_bishop_bb)
            black_attacking_bb |= bishop.bishop_attacks(bishop_1, self.all_pieces_bb)
            black_attacking_bb |= bishop.bishop_attacks(bishop_2, self.all_pieces_bb)

            rook_1, rook_2 = index_of_LSB(self.b_rook_bb), index_of_MSB(self.b_rook_bb)
            black_attacking_bb |= rook.rook_attacks(rook_1, self.all_pieces_bb)
            black_attacking_bb |= rook.rook_attacks(rook_2, self.all_pieces_bb)

            queen_1 = index_of_LSB(self.b_queen_bb)
            black_attacking_bb |= queen.queen_attacks(queen_1, self.all_pieces_bb)

            king_1 = index_of_LSB(self.b_king_bb)
            black_attacking_bb |= king.king_targets(king_1)

            return black_attacking_bb

    def material_eval(self):
        evalution = 0
        # Pawn material
        evalution += (PIECE_VALUES['P'] * bin(self.w_pawn_bb).count("1"))
        evalution -= (PIECE_VALUES['P'] * bin(self.b_pawn_bb).count("1"))

        # Knight material
        evalution += (PIECE_VALUES['N'] * bin(self.w_knight_bb).count("1"))
        evalution -= (PIECE_VALUES['N'] * bin(self.b_knight_bb).count("1"))
        
        # Bishop material
        evalution += (PIECE_VALUES['B'] * bin(self.w_bishop_bb).count("1"))
        evalution -= (PIECE_VALUES['B'] * bin(self.b_bishop_bb).count("1"))
        
        # Rook material
        evalution += (PIECE_VALUES['R'] * bin(self.w_rook_bb).count("1"))
        evalution -= (PIECE_VALUES['R'] * bin(self.b_rook_bb).count("1"))
        
        # Queen material
        evalution += PIECE_VALUES['Q'] if self.w_queen_bb else 0
        evalution -= PIECE_VALUES['Q'] if self.b_queen_bb else 0

        return evalution
    # .00025
    def get_legal_moves(self, white=True):
        moves = []
        if white:
            for idx in bitscan(self.w_pieces_bb):
                if get_bit(self.w_pieces_bb, idx):
                    # Pawn Move Generation
                    if self.w_pawn_bb & (1 << idx):
                        row, col = idx // 8, idx % 8  
                        if row < 6:
                            if not get_bit(self.all_pieces_bb, idx + 8):
                                moves.append({"piece": 'P', "start": idx, "end": idx + 8, "code": 0})
                            # Check if the pawn can move two squares forward from its starting position
                            if row == 1 and not get_bit(self.all_pieces_bb, idx + 16) and not get_bit(self.all_pieces_bb, idx + 8):
                                moves.append({"piece": 'P', "start": idx, "end": idx + 16, "code": 0})
                            # Check if the pawn can capture diagonally (left and right)
                            if col > 0 and get_bit(self.b_pieces_bb, idx + 7):
                                moves.append({"piece": 'P', "start": idx, "end": idx + 7, "code": 4})
                            if col < 7 and get_bit(self.b_pieces_bb, idx + 9):
                                moves.append({"piece": 'P', "start": idx, "end": idx + 9, "code": 4})
                            # Check if the pawn can ep capture 
                            if col > 0 and get_bit(self.en_passant_square, idx + 7):
                                moves.append({"piece": 'P', "start": idx, "end": idx + 7, "code": 5})
                            if col < 7 and get_bit(self.en_passant_square, idx + 9):
                                moves.append({"piece": 'P', "start": idx, "end": idx + 9, "code": 5})
                        else:  # PROMOTIONS
                            if not get_bit(self.all_pieces_bb, idx + 8):
                                moves.append({"piece": 'P', "start": idx, "end": idx + 8, "code": 8})
                                moves.append({"piece": 'P', "start": idx, "end": idx + 8, "code": 9})
                                moves.append({"piece": 'P', "start": idx, "end": idx + 8, "code": 10})
                                moves.append({"piece": 'P', "start": idx, "end": idx + 8, "code": 11})
                            # Check if the pawn can capture diagonally (left and right)
                            if col > 0 and get_bit(self.b_pieces_bb, idx + 7):
                                moves.append({"piece": 'P', "start": idx, "end": idx + 7, "code": 12})
                                moves.append({"piece": 'P', "start": idx, "end": idx + 7, "code": 13})
                                moves.append({"piece": 'P', "start": idx, "end": idx + 7, "code": 14})
                                moves.append({"piece": 'P', "start": idx, "end": idx + 7, "code": 15})
                            if col < 7 and get_bit(self.b_pieces_bb, idx + 9):
                                moves.append({"piece": 'P', "start": idx, "end": idx + 9, "code": 12})
                                moves.append({"piece": 'P', "start": idx, "end": idx + 9, "code": 13})
                                moves.append({"piece": 'P', "start": idx, "end": idx + 9, "code": 14})
                                moves.append({"piece": 'P', "start": idx, "end": idx + 9, "code": 15})
                    # Knight Move Generation
                    elif self.w_knight_bb & (1 << idx):
                        for end_idx in bitscan(knight.knight_moves(idx, self.w_pieces_bb)):
                            if get_bit(self.b_pieces_bb, end_idx):
                                moves.append({"piece": 'N', "start": idx, "end": end_idx, "code": 4})
                            else:
                                moves.append({"piece": 'N', "start": idx, "end": end_idx, "code": 0})
                    # Bishop Move Generation
                    elif self.w_bishop_bb & (1 << idx):
                        for end_idx in bitscan(bishop.bishop_moves(idx, self.w_pieces_bb, self.all_pieces_bb)):
                            if get_bit(self.b_pieces_bb, end_idx):
                                moves.append({"piece": 'B', "start": idx, "end": end_idx, "code": 4})
                            else:
                                moves.append({"piece": 'B', "start": idx, "end": end_idx, "code": 0})
                    # Rook Move Generation
                    elif self.w_rook_bb & (1 << idx):
                        for end_idx in bitscan(rook.rook_moves(idx, self.w_pieces_bb, self.all_pieces_bb)):
                            if get_bit(self.b_pieces_bb, end_idx):
                                moves.append({"piece": 'R', "start": idx, "end": end_idx, "code": 4})
                            else:
                                moves.append({"piece": 'R', "start": idx, "end": end_idx, "code": 0})
                    # Queen Move Generation
                    elif self.w_queen_bb & (1 << idx):
                        for end_idx in bitscan(queen.queen_moves(idx, self.w_pieces_bb, self.all_pieces_bb)):
                            if get_bit(self.b_pieces_bb, end_idx):
                                moves.append({"piece": 'Q', "start": idx, "end": end_idx, "code": 4})
                            else:
                                moves.append({"piece": 'Q', "start": idx, "end": end_idx, "code": 0})
                    # King Move Generation
                    elif self.w_king_bb & (1 << idx):
                        black_capturing_bb = self.get_attacking_bitboard(False)
                        for end_idx in bitscan(king.king_moves(idx, self.w_pieces_bb, black_capturing_bb)):
                            # Quiet moves and captures
                            if get_bit(self.b_pieces_bb, end_idx):
                                moves.append({"piece": 'K', "start": idx, "end": end_idx, "code": 4})
                            else:
                                moves.append({"piece": 'K', "start": idx, "end": end_idx, "code": 0})
                            # Castle
                            if self.castle_availability['K'] and not (constants.W_KING_CASTLE_CLEAR & self.all_pieces_bb):
                                moves.append({"piece": 'K', "code": 2})
                            if self.castle_availability['Q'] and not (constants.W_QUEEN_CASTLE_CLEAR & self.all_pieces_bb):
                                moves.append({"piece": 'K', "code": 3})
        else:
            for idx in bitscan(self.b_pieces_bb):
                if get_bit(self.b_pieces_bb, idx):
                    # Pawn Move Generation
                    if self.b_pawn_bb & (1 << idx):
                        row, col = idx // 8, idx % 8  
                        if row > 1:
                            if not get_bit(self.all_pieces_bb, idx - 8):
                                moves.append({"piece": 'p', "start": idx, "end": idx - 8, "code": 0})
                            # Check if the pawn can move two squares forward from its starting position
                            if row == 6 and not get_bit(self.all_pieces_bb, idx - 16) and not get_bit(self.all_pieces_bb, idx - 8):
                                moves.append({"piece": 'p', "start": idx, "end": idx - 16, "code": 0})
                            # Check if the pawn can capture diagonally (left and right)
                            if col < 7 and get_bit(self.w_pieces_bb, idx - 7):
                                moves.append({"piece": 'p', "start": idx, "end": idx - 7, "code": 4})
                            if col > 0 and get_bit(self.w_pieces_bb, idx - 9):
                                moves.append({"piece": 'p', "start": idx, "end": idx - 9, "code": 4})
                            # Check if the pawn can ep capture 
                            if col < 7 and get_bit(self.en_passant_square, idx - 7):
                                moves.append({"piece": 'p', "start": idx, "end": idx - 7, "code": 5})
                            if col > 0 and get_bit(self.en_passant_square, idx - 9):
                                moves.append({"piece": 'p', "start": idx, "end": idx - 9, "code": 5})
                        else:  # PROMOTIONS
                            if not get_bit(self.all_pieces_bb, idx - 8):
                                moves.append({"piece": 'p', "start": idx, "end": idx - 8, "code": 8})
                                moves.append({"piece": 'p', "start": idx, "end": idx - 8, "code": 9})
                                moves.append({"piece": 'p', "start": idx, "end": idx - 8, "code": 10})
                                moves.append({"piece": 'p', "start": idx, "end": idx - 8, "code": 11})
                            # Check if the pawn can capture diagonally (left and right)
                            if col < 7 and get_bit(self.b_pieces_bb, idx - 7):
                                moves.append({"piece": 'p', "start": idx, "end": idx - 7, "code": 12})
                                moves.append({"piece": 'p', "start": idx, "end": idx - 7, "code": 13})
                                moves.append({"piece": 'p', "start": idx, "end": idx - 7, "code": 14})
                                moves.append({"piece": 'p', "start": idx, "end": idx - 7, "code": 15})
                            if col > 0 and get_bit(self.b_pieces_bb, idx - 9):
                                moves.append({"piece": 'p', "start": idx, "end": idx - 9, "code": 12})
                                moves.append({"piece": 'p', "start": idx, "end": idx - 9, "code": 13})
                                moves.append({"piece": 'p', "start": idx, "end": idx - 9, "code": 14})
                                moves.append({"piece": 'p', "start": idx, "end": idx - 9, "code": 15})
                    # Knight Move Generation
                    elif self.b_knight_bb & (1 << idx):
                        for end_idx in bitscan(knight.knight_moves(idx, self.b_pieces_bb)):
                            if get_bit(self.w_pieces_bb, end_idx):
                                moves.append({"piece": 'n', "start": idx, "end": end_idx, "code": 4})
                            else:
                                moves.append({"piece": 'n', "start": idx, "end": end_idx, "code": 0})
                    # Bishop Move Generation
                    elif self.b_bishop_bb & (1 << idx):
                        for end_idx in bitscan(bishop.bishop_moves(idx, self.b_pieces_bb, self.all_pieces_bb)):
                            if get_bit(self.w_pieces_bb, end_idx):
                                moves.append({"piece": 'b', "start": idx, "end": end_idx, "code": 4})
                            else:
                                moves.append({"piece": 'b', "start": idx, "end": end_idx, "code": 0})            
                    # Rook Move Generation
                    elif self.b_rook_bb & (1 << idx):
                        for end_idx in bitscan(rook.rook_moves(idx, self.b_pieces_bb, self.all_pieces_bb)):
                            if get_bit(self.w_pieces_bb, end_idx):
                                moves.append({"piece": 'r', "start": idx, "end": end_idx, "code": 4})
                            else:
                                moves.append({"piece": 'r', "start": idx, "end": end_idx, "code": 0})
                    # Queen Move Generation
                    elif self.b_queen_bb & (1 << idx):
                        for end_idx in bitscan(queen.queen_moves(idx, self.b_pieces_bb, self.all_pieces_bb)):
                            if get_bit(self.w_pieces_bb, end_idx):
                                moves.append({"piece": 'q', "start": idx, "end": end_idx, "code": 4})
                            else:
                                moves.append({"piece": 'q', "start": idx, "end": end_idx, "code": 0})
                    # King Move Generation
                    elif self.b_king_bb & (1 << idx):
                        white_capturing_bb = self.get_attacking_bitboard(True)
                        for end_idx in bitscan(king.king_moves(idx, self.b_pieces_bb, white_capturing_bb)):
                            # Quiet moves and captures
                            if get_bit(self.w_pieces_bb, end_idx):
                                moves.append({"piece": 'k', "start": idx, "end": end_idx, "code": 4})
                            else:
                                moves.append({"piece": 'k', "start": idx, "end": end_idx, "code": 0})
                            # Castle
                            if self.castle_availability['k'] and not (constants.B_KING_CASTLE_CLEAR & self.all_pieces_bb):
                                moves.append({"piece": 'k', "code": 2})
                            if self.castle_availability['q'] and not (constants.B_QUEEN_CASTLE_CLEAR & self.all_pieces_bb):
                                moves.append({"piece": 'k', "code": 3})
            return moves



b = Position()

start = time.time()
# bitboard_to_board(bin(knight.w_knight_targets(25, b.w_pieces_bb)))
#bitboard_to_board(bin(bishop.bishop_moves(2, b.all_pieces_bb, b.all_pieces_bb)))
# bitboard_to_board(bin(rook.w_rook_attacks(37, b.w_pieces_bb, b.all_pieces_bb)))
# bitboard_to_board(bin(queen.b_queen_attacks(35, b.b_pieces_bb, b.all_pieces_bb)))
# bitboard_to_board(bin(b.get_attacking_bitboard(white=True)))
print(len(b.get_legal_moves(False)))
print(time.time() - start)

