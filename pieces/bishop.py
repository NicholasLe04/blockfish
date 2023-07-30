from bitboard_util import set_bit, index_of_LSB, index_of_MSB
import math

def _get_NW_bitboard(start_index):
    NW_ray = int("00000000_00000000_00000000_00000000_00000000_00000000_00000000_00000000", 2)
    for i in range(start_index+9, 64, 9):
        if abs(i//8 - (i-9)//8) != 1 or abs(i%8 - (i-9)%8) != 1:
            break
        NW_ray = set_bit(NW_ray, i)
    return NW_ray

def _get_NE_bitboard(start_index):
    NE_ray = int("00000000_00000000_00000000_00000000_00000000_00000000_00000000_00000000", 2)
    for i in range(start_index+7, 64, 7):
        if abs(i//8 - (i-7)//8) != 1 or abs(i%8 - (i-7)%8) != 1:
            break
        NE_ray = set_bit(NE_ray, i)
    return NE_ray

def _get_SW_bitboard(start_index):
    SW_ray = int("00000000_00000000_00000000_00000000_00000000_00000000_00000000_00000000", 2)
    for i in range(start_index-7, -1, -7):
        if abs(i//8 - (i+7)//8) != 1 or abs(i%8 - (i+7)%8) != 1:
            break
        SW_ray = set_bit(SW_ray, i)
    return SW_ray

def _get_SE_bitboard(start_index):
    SE_ray = int("00000000_00000000_00000000_00000000_00000000_00000000_00000000_00000000", 2)
    for i in range(start_index-9, -1, -9):
        if abs(i//8 - (i+9)//8) != 1 or abs(i%8 - (i+9)%8) != 1:
            break
        SE_ray = set_bit(SE_ray, i)
    return SE_ray


def bishop_attacks(start_index, all_pieces):
    w_bishop_targets = 0

    # Northwest Ray 
    NW_ray = _get_NW_bitboard(start_index)
    blockers = NW_ray & all_pieces
    if blockers != 0:
        lsb_index = index_of_LSB(blockers)
        w_bishop_targets |= (_get_NW_bitboard(lsb_index) ^ NW_ray)
    else:
        w_bishop_targets |= NW_ray
    
    # Northeast Ray 
    NE_ray = _get_NE_bitboard(start_index)
    blockers = NE_ray & all_pieces
    if blockers != 0:
        lsb_index = index_of_LSB(blockers)
        w_bishop_targets |= (_get_NE_bitboard(lsb_index) ^ NE_ray)
    else:
        w_bishop_targets |= NE_ray
    
    # Southwest Ray 
    SW_ray = _get_SW_bitboard(start_index)
    blockers = SW_ray & all_pieces
    if blockers != 0:
        msb_index = index_of_MSB(blockers)
        w_bishop_targets |= (_get_SW_bitboard(msb_index) ^ SW_ray)
    else:
        w_bishop_targets |= SW_ray
        
    # Southeast Ray 
    SE_ray = _get_SE_bitboard(start_index)
    blockers = SE_ray & all_pieces
    if blockers != 0:
        msb_index = index_of_MSB(blockers)
        w_bishop_targets |= (_get_SE_bitboard(msb_index) ^ SE_ray)
    else:
        w_bishop_targets |= SE_ray

    return w_bishop_targets


