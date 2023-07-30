from constants import KNIGHT_ATTACKS
from bitboard_util import get_bit

def knight_attacks(start_index, ):
    return (KNIGHT_ATTACKS[start_index])

def knight_moves(start_index, friendly_pieces):
    return (knight_attacks(start_index) & ~friendly_pieces)
        
