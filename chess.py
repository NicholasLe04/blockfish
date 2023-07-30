import pieces.pawn as pawn
import pieces.knight as knight
import pieces.bishop as bishop
import pieces.rook as rook
import pieces.queen as queen
import pieces.king as king

from bitboard_util import bitboard_to_board, index_of_MSB, index_of_LSB

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

        self.all_pieces_bb = (self.w_pawn_bb | self.w_knight_bb | self.w_bishop_bb | self.w_rook_bb | self.w_queen_bb | self.b_king_bb |
                               self.b_pawn_bb | self.b_knight_bb | self.b_bishop_bb | self.b_rook_bb | self.b_queen_bb | self.b_king_bb)

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
            white_attacking_bb |= queen.queen_moves(queen_1, self.all_pieces_bb)

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
            black_attacking_bb |= queen.queen_moves(queen_1, self.all_pieces_bb)

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
    
b = Position()

start = time.time()
# bitboard_to_board(bin(knight.w_knight_targets(25, b.w_pieces_bb)))
# bitboard_to_board(bin(bishop.b_bishop_attacks(33, b.b_pieces_bb, b.all_pieces_bb)))
# bitboard_to_board(bin(rook.w_rook_attacks(37, b.w_pieces_bb, b.all_pieces_bb)))
# bitboard_to_board(bin(queen.b_queen_attacks(35, b.b_pieces_bb, b.all_pieces_bb)))
bitboard_to_board(bin(b.get_attacking_bitboard(False)))
print(time.time() - start)

