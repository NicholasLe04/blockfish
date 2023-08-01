from constants import RANK_4, RANK_5, EXCLUDE_A_FILE, EXCLUDE_H_FILE

# White pushes
def w_pawn_single_push_targets(w_pawn_bb, all_pieces_bb):
    empty_bb = ~all_pieces_bb
    return (w_pawn_bb << 8) & empty_bb

def w_pawn_double_push_targets(w_pawn_bb, all_pieces_bb):
    empty_bb = ~all_pieces_bb
    single_push = w_pawn_single_push_targets(w_pawn_bb, all_pieces_bb)
    return (single_push << 8) & empty_bb & RANK_4


# White Captures
def _w_pawn_east_attacks(w_pawn_bb):
    return ((w_pawn_bb << 7) & EXCLUDE_A_FILE)

def _w_pawn_west_attacks(w_pawn_bb):
    return ((w_pawn_bb << 9) & EXCLUDE_H_FILE)

def w_pawn_attacks(w_pawn_bb):
    return _w_pawn_west_attacks(w_pawn_bb) | _w_pawn_east_attacks(w_pawn_bb)

def w_pawn_captures(w_pawn_bb, b_pieces_bb):
    return w_pawn_attacks(w_pawn_bb) & b_pieces_bb


# Black Pushes
def b_pawn_single_push_targets(b_pawn_bb, all_pieces_bb):
    empty_bb = ~all_pieces_bb
    return (b_pawn_bb >> 8) & empty_bb

def b_pawn_double_push_targets(b_pawn_bb, all_pieces_bb):
    empty_bb = ~all_pieces_bb
    single_push = b_pawn_single_push_targets(b_pawn_bb, all_pieces_bb)
    return (single_push >> 8) & empty_bb & RANK_5


# Black Captures
def _b_pawn_east_attacks(b_pawn_bb):
    return ((b_pawn_bb >> 9) & EXCLUDE_A_FILE)

def _b_pawn_west_attacks(b_pawn_bb):
    return ((b_pawn_bb >> 7) & EXCLUDE_H_FILE)

def b_pawn_attacks(b_pawn_bb):
    return _b_pawn_west_attacks(b_pawn_bb) | _b_pawn_east_attacks(b_pawn_bb)

def b_pawn_captures(b_pawn_bb, w_pieces_bb):
    return b_pawn_attacks(b_pawn_bb) & w_pieces_bb
