from engine.constants import KNIGHT_TARGETS
from engine.bitboard_util import get_bit

def knight_attacks(start_index, ):
    return (KNIGHT_TARGETS[start_index])

def knight_moves(start_index, friendly_pieces):
    return (knight_attacks(start_index) & ~friendly_pieces)
        
