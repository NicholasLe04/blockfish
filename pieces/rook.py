from bitboard_util import set_bit, index_of_LSB, index_of_MSB


def _get_N_bitboard(start_index):
    N_ray = int("00000000_00000000_00000000_00000000_00000000_00000000_00000000_00000000", 2)
    for i in range(start_index+8, 64, 8):
        N_ray = set_bit(N_ray, i)
    return N_ray

def _get_W_bitboard(start_index):
    W_ray = int("00000000_00000000_00000000_00000000_00000000_00000000_00000000_00000000", 2)
    for i in range(start_index+1, start_index+8, 1):
        if abs(i//8 - (i-1)//8) != 0:
            break
        W_ray = set_bit(W_ray, i)
    return W_ray

def _get_S_bitboard(start_index):
    S_ray = int("00000000_00000000_00000000_00000000_00000000_00000000_00000000_00000000", 2)
    for i in range(start_index-8, -1, -8):
        S_ray = set_bit(S_ray, i)
    return S_ray
def _get_E_bitboard(start_index):
    E_ray = int("00000000_00000000_00000000_00000000_00000000_00000000_00000000_00000000", 2)
    for i in range(start_index-1, start_index-8, -1):
        if abs(i//8 - (i+1)//8) != 0:
            break
        E_ray = set_bit(E_ray, i)
    return E_ray

def rook_attacks(start_index, all_pieces):
    # North ray
    rook_targets = 0
    N_ray = _get_N_bitboard(start_index)
    blockers = N_ray & all_pieces
    if blockers != 0:
        lsb_index = index_of_LSB(blockers)
        rook_targets |= (_get_N_bitboard(lsb_index) ^ N_ray)
    else:
        rook_targets |= N_ray

    # West ray
    W_ray = _get_W_bitboard(start_index)
    blockers = W_ray & all_pieces
    if blockers != 0:
        lsb_index = index_of_LSB(blockers)
        rook_targets |= (_get_W_bitboard(lsb_index) ^ W_ray)
    else:
        rook_targets |= W_ray

    # South Ray
    S_ray = _get_S_bitboard(start_index)
    blockers = S_ray & all_pieces
    if blockers != 0:
        msb_index = index_of_MSB(blockers)
        rook_targets |= (_get_S_bitboard(msb_index) ^ S_ray)
    else:
        rook_targets |= S_ray

    # East Ray
    E_ray = _get_E_bitboard(start_index)
    blockers = E_ray & all_pieces
    if blockers != 0:
        msb_index = index_of_MSB(blockers)
        rook_targets |= (_get_E_bitboard(msb_index) ^ E_ray)
    else:
        rook_targets |= E_ray

    return rook_targets

def rook_moves(start_index, friendly_pieces, all_pieces):
    return rook_attacks(start_index, all_pieces) & ~friendly_pieces
