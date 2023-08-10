from bitboard_util import set_bit

def king_targets(start_index):
    king_targets_bb = int("00000000_00000000_00000000_00000000_00000000_00000000_00000000_00000000", 2)
    
    for dir in [9, 8, 7, -1, 1, -7, -8, -9]:
        end_index = start_index + dir
        if 0 <= end_index < 64 and abs(end_index//8 - start_index//8) <= 1 and abs(end_index%8 - start_index%8) <= 1:
            king_targets_bb = set_bit(king_targets_bb, end_index)

    return king_targets_bb

def king_moves(start_index, friendly_pieces):
    return king_targets(start_index) & ~friendly_pieces
