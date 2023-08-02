from bitboard_util import set_bit

INDEX_TO_POSITION = {
       63: 'h1', 62: 'h2', 61: 'h3', 60: 'h4', 59: 'h5', 58: 'h6', 57: 'h7', 56: 'h8',
       55: 'g1', 54: 'g2', 53: 'g3', 52: 'g4', 51: 'g5', 50: 'g6', 49: 'g7', 48: 'g8',
       47: 'f1', 46: 'f2', 45: 'f3', 44: 'f4', 43: 'f5', 42: 'f6', 41: 'f7', 40: 'f8',
       39: 'e1', 38: 'e2', 37: 'e3', 36: 'e4', 35: 'e5', 34: 'e6', 33: 'e7', 32: 'e8',
       31: 'd1', 30: 'd2', 29: 'd3', 28: 'd4', 27: 'd5', 26: 'd6', 25: 'd7', 24: 'd8',
       23: 'c1', 22: 'c2', 21: 'c3', 20: 'c4', 19: 'c5', 18: 'c6', 17: 'c7', 16: 'c8',
       15: 'b1', 14: 'b2', 13: 'b3', 12: 'b4', 11: 'b5', 10: 'b6', 9:  'b7', 8:  'b8',
       7:  'a1', 6: ' a2', 5:  'a3', 4:  'a4', 3:  'a5', 2:  'a6', 1:  'a7', 0:  'a8'
   }

POSITION_TO_INDEX  = {
        'h1': 63, 'h2': 62, 'h3': 61, 'h4': 60, 'h5': 59, 'h6': 58, 'h7': 57, 'h8': 56,
        'g1': 55, 'g2': 54, 'g3': 53, 'g4': 52, 'g5': 51, 'g6': 50, 'g7': 49, 'g8': 48,
        'f1': 47, 'f2': 46, 'f3': 45, 'f4': 44, 'f5': 43, 'f6': 42, 'f7': 41, 'f8': 40,
        'e1': 39, 'e2': 38, 'e3': 37, 'e4': 36, 'e5': 35, 'e6': 34, 'e7': 33, 'e8': 32,
        'd1': 31, 'd2': 30, 'd3': 29, 'd4': 28, 'd5': 27, 'd6': 26, 'd7': 25, 'd8': 24,
        'c1': 23, 'c2': 22, 'c3': 21, 'c4': 20, 'c5': 19, 'c6': 18, 'c7': 17, 'c8': 16,
        'b1': 15, 'b2': 14, 'b3': 13, 'b4': 12, 'b5': 11, 'b6': 10, 'b7': 9 , 'b8': 8 ,
        'a1': 7,  'a2': 6 , 'a3': 5 , 'a4': 4 , 'a5': 3 , 'a6': 2 , 'a7': 1 , 'a8': 0 
   }

EXCLUDE_A_FILE = 0x7F7F7F7F7F7F7F7F         # 01111111_01111111_01111111_01111111_01111111_01111111_01111111_01111111
EXCLUDE_H_FILE = 0xFEFEFEFEFEFEFEFE         # 11111110_11111110_11111110_11111110_11111110_11111110_11111110_11111110

RANK_4 = 0xFF000000                         # 00000000_00000000_00000000_00000000_11111111_00000000_00000000_00000000
RANK_5 = 0xFF00000000                       # 00000000_00000000_00000000_11111111_00000000_00000000_00000000_00000000

W_KING_CASTLE_CLEAR =  0x6                  # 00000000_00000000_00000000_00000000_00000000_00000000_00000000_00000110
W_QUEEN_CASTLE_CLEAR = 0x70                 # 00000000_00000000_00000000_00000000_00000000_00000000_00000000_01110000
B_KING_CASTLE_CLEAR =  0x600000000000000    # 00000110_00000000_00000000_00000000_00000000_00000000_00000000_00000000
B_QUEEN_CASTLE_CLEAR = 0x7000000000000000   # 01110000_00000000_00000000_00000000_00000000_00000000_00000000_00000000


PIECE_VALUES = { 
                'P': 1, 
                'N': 3.05,
                'B': 3.33, 
                'R': 5.63, 
                'Q': 9.5, 
                'K': 0, 
                } # Per AlphaZero


###################
#   ATTACK MAPS
###################

def _get_NW_bitboard(start_index):
    NW_ray = 0x0
    for i in range(start_index+9, 64, 9):
        if abs(i//8 - (i-9)//8) != 1 or abs(i%8 - (i-9)%8) != 1:
            break
        NW_ray = set_bit(NW_ray, i)
    return NW_ray

def _get_NE_bitboard(start_index):
    NE_ray = 0x0
    for i in range(start_index+7, 64, 7):
        if abs(i//8 - (i-7)//8) != 1 or abs(i%8 - (i-7)%8) != 1:
            break
        NE_ray = set_bit(NE_ray, i)
    return NE_ray

def _get_SW_bitboard(start_index):
    SW_ray = 0x0
    for i in range(start_index-7, -1, -7):
        if abs(i//8 - (i+7)//8) != 1 or abs(i%8 - (i+7)%8) != 1:
            break
        SW_ray = set_bit(SW_ray, i)
    return SW_ray

def _get_SE_bitboard(start_index):
    SE_ray = 0x0
    for i in range(start_index-9, -1, -9):
        if abs(i//8 - (i+9)//8) != 1 or abs(i%8 - (i+9)%8) != 1:
            break
        SE_ray = set_bit(SE_ray, i)
    return SE_ray


def _get_N_bitboard(start_index):
    N_ray = 0x0
    for i in range(start_index+8, 64, 8):
        N_ray = set_bit(N_ray, i)
    return N_ray

def _get_W_bitboard(start_index):
    W_ray = 0x0
    for i in range(start_index+1, start_index+8, 1):
        if abs(i//8 - (i-1)//8) != 0:
            break
        W_ray = set_bit(W_ray, i)
    return W_ray

def _get_S_bitboard(start_index):
    S_ray = 0x0
    for i in range(start_index-8, -1, -8):
        S_ray = set_bit(S_ray, i)
    return S_ray
def _get_E_bitboard(start_index):
    E_ray = 0x0
    for i in range(start_index-1, start_index-8, -1):
        if abs(i//8 - (i+1)//8) != 0:
            break
        E_ray = set_bit(E_ray, i)
    return E_ray

KNIGHT_TARGETS = {}

for start_index in range(64):
    KNIGHT_TARGETS[start_index] = 0x0
    for dir in [17, 15, 10, 6, -6, -10, -15, -17]:
        if 0 <= start_index + dir < 64 and (-2 <= (start_index+dir)//8 - start_index//8 <= 2) and (-2 <= (start_index+dir)%8 - start_index%8 <= 2):
            KNIGHT_TARGETS[start_index] = set_bit(KNIGHT_TARGETS[start_index], start_index + dir)

BISHOP_TARGETS = { 
                    "NW": {}, 
                    "NE": {}, 
                    "SE": {}, 
                    "SW": {},
                 }

for start_index in range(64):
    BISHOP_TARGETS["NW"][start_index] = _get_NW_bitboard(start_index)
    BISHOP_TARGETS["NE"][start_index] = _get_NE_bitboard(start_index)
    BISHOP_TARGETS["SE"][start_index] = _get_SE_bitboard(start_index)
    BISHOP_TARGETS["SW"][start_index] = _get_SW_bitboard(start_index)

ROOK_TARGETS = { 
                "N": {}, 
                "E": {}, 
                "S": {}, 
                "W": {},
             }

for start_index in range(64):
    ROOK_TARGETS["N"][start_index] = _get_N_bitboard(start_index)
    ROOK_TARGETS["E"][start_index] = _get_E_bitboard(start_index)
    ROOK_TARGETS["S"][start_index] = _get_S_bitboard(start_index)
    ROOK_TARGETS["W"][start_index] = _get_W_bitboard(start_index)

# code	promotion	capture	special 1	special 0	kind of move
# 0	    0	        0	    0	        0	        quiet moves
# 1	    0	        0	    0	        1	        double pawn push
# 2	    0	        0	    1	        0	        king castle
# 3	    0	        0	    1	        1	        queen castle
# 4	    0	        1	    0	        0	        captures
# 5	    0	        1	    0	        1	        ep-capture
# 8	    1	        0	    0	        0	        knight-promotion
# 9	    1	        0	    0	        1	        bishop-promotion
# 10	1	        0	    1	        0	        rook-promotion
# 11	1	        0	    1	        1	        queen-promotion
# 12	1	        1	    0	        0	        knight-promo capture
# 13	1	        1	    0	        1	        bishop-promo capture
# 14	1	        1	    1	        0	        rook-promo capture
# 15	1	        1	    1	        1	        queen-promo capture
