from bitboard_util import index_of_LSB, index_of_MSB
from constants import ROOK_ATTACKS

def rook_attacks(start_index, all_pieces):
    # North ray
    rook_targets = 0
    N_ray = ROOK_ATTACKS["N"][start_index]
    blockers = N_ray & all_pieces
    if blockers != 0:
        lsb_index = index_of_LSB(blockers)
        rook_targets |= (ROOK_ATTACKS["N"][lsb_index] ^ N_ray)
    else:
        rook_targets |= N_ray

    # West ray
    W_ray = ROOK_ATTACKS["W"][start_index]
    blockers = W_ray & all_pieces
    if blockers != 0:
        lsb_index = index_of_LSB(blockers)
        rook_targets |= (ROOK_ATTACKS["W"][lsb_index] ^ W_ray)
    else:
        rook_targets |= W_ray

    # South Ray
    S_ray = ROOK_ATTACKS["S"][start_index]
    blockers = S_ray & all_pieces
    if blockers != 0:
        msb_index = index_of_MSB(blockers)
        rook_targets |= (ROOK_ATTACKS["S"][msb_index] ^ S_ray)
    else:
        rook_targets |= S_ray

    # East Ray
    E_ray = ROOK_ATTACKS["E"][start_index]
    blockers = E_ray & all_pieces
    if blockers != 0:
        msb_index = index_of_MSB(blockers)
        rook_targets |= (ROOK_ATTACKS["E"][msb_index] ^ E_ray)
    else:
        rook_targets |= E_ray

    return rook_targets

def rook_moves(start_index, friendly_pieces, all_pieces):
    return rook_attacks(start_index, all_pieces) & ~friendly_pieces
