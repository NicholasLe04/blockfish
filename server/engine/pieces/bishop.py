from engine.bitboard_util import index_of_LSB, index_of_MSB
from engine.constants import BISHOP_TARGETS

def bishop_attacks(start_index, all_pieces):
    bishop_targets = 0

    # Northwest Ray 
    NW_ray = BISHOP_TARGETS['NW'][start_index]
    blockers = NW_ray & all_pieces
    if blockers != 0:
        lsb_index = index_of_LSB(blockers)
        bishop_targets |= (BISHOP_TARGETS['NW'][lsb_index] ^ NW_ray)
    else:
        bishop_targets |= NW_ray
    
    # Northeast Ray 
    NE_ray = BISHOP_TARGETS['NE'][start_index]
    blockers = NE_ray & all_pieces
    if blockers != 0:
        lsb_index = index_of_LSB(blockers)
        bishop_targets |= (BISHOP_TARGETS['NE'][lsb_index] ^ NE_ray)
    else:
        bishop_targets |= NE_ray
    
    # Southwest Ray 
    SW_ray = BISHOP_TARGETS['SW'][start_index]
    blockers = SW_ray & all_pieces
    if blockers != 0:
        msb_index = index_of_MSB(blockers)
        bishop_targets |= (BISHOP_TARGETS['SW'][msb_index] ^ SW_ray)
    else:
        bishop_targets |= SW_ray
        
    # Southeast Ray 
    SE_ray = BISHOP_TARGETS['SE'][start_index]
    blockers = SE_ray & all_pieces
    if blockers != 0:
        msb_index = index_of_MSB(blockers)
        bishop_targets |= (BISHOP_TARGETS['SE'][msb_index] ^ SE_ray)
    else:
        bishop_targets |= SE_ray

    return bishop_targets

def bishop_moves(start_index, friendly_pieces, all_pieces):
    return bishop_attacks(start_index, all_pieces) & ~friendly_pieces

