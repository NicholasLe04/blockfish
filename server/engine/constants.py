from engine.bitboard_util import set_bit
import uuid

# Zobrist Hashing Table
ZOBRIST_HASH_TABLE = []

for cell in range(64):
    ZOBRIST_HASH_TABLE.append([])
    for piece in range(12):
        ZOBRIST_HASH_TABLE[cell].append(uuid.uuid1().int>>64)

INDEX_TO_POSITION = {
       63: 'a8', 62: 'b8', 61: 'c8', 60: 'd8', 59: 'e8', 58: 'f8', 57: 'g8', 56: 'h8',
       55: 'a7', 54: 'b7', 53: 'c7', 52: 'd7', 51: 'e7', 50: 'f7', 49: 'g7', 48: 'h7',
       47: 'a6', 46: 'b6', 45: 'c6', 44: 'd6', 43: 'e6', 42: 'f6', 41: 'g6', 40: 'h6',
       39: 'a5', 38: 'b5', 37: 'c5', 36: 'd5', 35: 'e5', 34: 'f5', 33: 'g5', 32: 'h5',
       31: 'a4', 30: 'b4', 29: 'c4', 28: 'd4', 27: 'e4', 26: 'f4', 25: 'g4', 24: 'h4',
       23: 'a3', 22: 'b3', 21: 'c3', 20: 'd3', 19: 'e3', 18: 'f3', 17: 'g3', 16: 'h3',
       15: 'a2', 14: 'b2', 13: 'c2', 12: 'd2', 11: 'e2', 10: 'f2', 9:  'g2', 8:  'h2',
       7:  'a1', 6:  'b1', 5:  'c1', 4:  'd1', 3:  'e1', 2:  'f1', 1:  'g1', 0:  'h1'
   }

POSITION_TO_INDEX  = {
       'a8': 63, 'b8': 62, 'c8': 61, 'd8': 60, 'e8': 59, 'f8': 58, 'g8': 57, 'h8': 56,
       'a7': 55, 'b7': 54, 'c7': 53, 'd7': 52, 'e7': 51, 'f7': 50, 'g7': 49, 'h7': 48,
       'a6': 47, 'b6': 46, 'c6': 45, 'd6': 44, 'e6': 43, 'f6': 42, 'g6': 41, 'h6': 40,
       'a5': 39, 'b5': 38, 'c5': 37, 'd5': 36, 'e5': 35, 'f5': 34, 'g5': 33, 'h5': 32,
       'a4': 31, 'b4': 30, 'c4': 29, 'd4': 28, 'e4': 27, 'f4': 26, 'g4': 25, 'h4': 24,
       'a3': 23, 'b3': 22, 'c3': 21, 'd3': 20, 'e3': 19, 'f3': 18, 'g3': 17, 'h3': 16,
       'a2': 15, 'b2': 14, 'c2': 13, 'd2': 12, 'e2': 11, 'f2': 10, 'g2': 9 , 'h2': 8 ,
       'a1':  7, 'b1': 6 , 'c1': 5 , 'd1': 4 , 'e1': 3 , 'f1': 2 , 'g1': 1 , 'h1': 0 
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

PIECE_TO_INDEX = {
                    'P': 0,
                    'N': 1,
                    'B': 2,
                    'R': 3,
                    'Q': 4,
                    'K': 5,
                    'p': 6,
                    'n': 7,
                    'b': 8,
                    'r': 9,
                    'q': 10,
                    'k': 11,
}

GAME_HEAT_MAP =   {
                            'P': [
                                    0,    0,    0,    0,    0,    0,    0,    0,   
                                    0,    0,    0,    0,    0,    0,    0,    0,   
                                    0,    0,    0.25, 0.25, 0.25, 0.25, 0,    0,   
                                    0,    0,    0.25, 0.50, 0.50, 0.25, 0,    0,   
                                    0,    0,    0.25, 0.50, 0.50, 0.25, 0,    0,   
                                    0,    0,    0.25, 0.25, 0.25, 0.25, 0,    0,   
                                    0,    0,    0,    0,    0,    0,    0,    0,   
                                    0,    0,    0,    0,    0,    0,    0,    0,   
                                ],
                            'p': [
                                    0,    0,    0,    0,    0,    0,    0,    0,   
                                    0,    0,    0,    0,    0,    0,    0,    0,   
                                    0,    0,    0.25, 0.25, 0.25, 0.25, 0,    0,   
                                    0,    0,    0.25, 0.50, 0.50, 0.25, 0,    0,   
                                    0,    0,    0.25, 0.50, 0.50, 0.25, 0,    0,   
                                    0,    0,    0.25, 0.25, 0.25, 0.25, 0,    0,   
                                    0,    0,    0,    0,    0,    0,    0,    0,   
                                    0,    0,    0,    0,    0,    0,    0,    0,   
                                ],
                            'N': [
                                    0,    0,    0,    0,    0,    0,    0,    0,   
                                    0,    0,    0,    0,    0,    0,    0,    0,   
                                    0,    0,    0,    0,    0,    0,    0,    0,   
                                    0,    0,    0,    0,    0,    0,    0,    0,   
                                    0,    0,    0,    0,    0,    0,    0,    0,   
                                    0,    0,    0.25, 0,    0,    0.25, 0,    0,   
                                    0,    0,    0,    0.1,  0.1,  0,    0,    0,   
                                    0,    0,    0,    0,    0,    0,    0,    0,  
                                ],
                            'n': [
                                    0,    0,    0,    0,    0,    0,    0,    0,   
                                    0,    0,    0,    0.1,  0.1,  0,    0,    0,   
                                    0,    0,    0.25, 0,    0,    0.25, 0,    0,   
                                    0,    0,    0,    0,    0,    0,    0,    0,   
                                    0,    0,    0,    0,    0,    0,    0,    0,   
                                    0,    0,    0,    0,    0,    0,    0,    0,   
                                    0,    0,    0,    0,    0,    0,    0,    0,   
                                    0,    0,    0,    0,    0,    0,    0,    0,  
                                ],
                            'B': [
                                    0,    0,    0,    0,    0,    0,    0,    0,    
                                    0,    0,    0,    0,    0,    0,    0,    0,
                                    0,    0,    0,    0,    0,    0,    0,    0,
                                    0,    0.25, 0,    0,    0,    0,    0.25, 0,   
                                    0,    0,    0.25, 0,    0,    0.25, 0,    0,        
                                    0,    0,    0,    0.25, 0.25, 0,    0,    0,  
                                    0,    0.25, 0,    0.25, 0.25, 0,    0.25, 0,    
                                    0,    0,    0,    0,    0,    0,    0,    0,  
                                ],
                            'b': [
                                    0,    0,    0,    0,    0,    0,    0,    0,   
                                    0,    0.25, 0,    0.25, 0.25, 0,    0.25, 0,   
                                    0,    0,    0,    0.25, 0.25, 0,    0,    0,   
                                    0,    0,    0.25, 0,    0,    0.25, 0,    0,   
                                    0,    0.25, 0,    0,    0,    0,    0.25, 0,   
                                    0,    0,    0,    0,    0,    0,    0,    0,   
                                    0,    0,    0,    0,    0,    0,    0,    0,   
                                    0,    0,    0,    0,    0,    0,    0,    0,  
                                ],
                            'R': [
                                    0,    0,    0,    0,    0,    0,    0,    0,   
                                    0,    0,    0,    0,    0,    0,    0,    0,    
                                    0,    0,    0,    0,    0,    0,    0,    0,   
                                    0,    0,    0,    0,    0,    0,    0,    0,    
                                    0.5,  0,    0,    0,    0,    0,    0,    0.5,    
                                    0.5,  0,    0,    0,    0,    0,    0,    0.5,   
                                    0.5,  0,    0,    0,    0,    0,    0,    0.5,   
                                    0.5,  0.5,  0.5,  0,    0,    0.5,  0.5,  0.5,  
                                ],
                            'r': [
                                    0.5,  0.5,  0.5,  0,    0,    0.5,  0.5,  0.5,   
                                    0.5,  0,    0,    0,    0,    0,    0,    0.5,   
                                    0.5,  0,    0,    0,    0,    0,    0,    0.5,   
                                    0.5,  0,    0,    0,    0,    0,    0,    0.5,   
                                    0,    0,    0,    0,    0,    0,    0,    0, 
                                    0,    0,    0,    0,    0,    0,    0,    0,  
                                    0,    0,    0,    0,    0,    0,    0,    0,      
                                    0,    0,    0,    0,    0,    0,    0,    0,  
                                ],
                            'Q': [
                                    0,    0,    0,    0,    0,    0,    0,    0,   
                                    0,    0,    0,    0,    0,    0,    0,    0,   
                                    0,    0,    0,    0,    0,    0,    0,    0,   
                                    0,    0,    0,    0,    0,    0,    0,    0,   
                                    0,    0,    0,    0,    0,    0,    0,    0,   
                                    0,    0,    0.25, 0.25, 0.25, 0.25, 0,    0,   
                                    0,    0,    0.25, 0.25, 0.25, 0.25, 0,    0,   
                                    0,    0,    0.25, 0.25, 0.25, 0.25, 0,    0,  
                                ],
                            'q': [
                                    0,    0,    0.25, 0.25, 0.25, 0.25, 0,    0,   
                                    0,    0,    0.25, 0.25, 0.25, 0.25, 0,    0,   
                                    0,    0,    0.25, 0.25, 0.25, 0.25, 0,    0,  
                                    0,    0,    0,    0,    0,    0,    0,    0,   
                                    0,    0,    0,    0,    0,    0,    0,    0,   
                                    0,    0,    0,    0,    0,    0,    0,    0,   
                                    0,    0,    0,    0,    0,    0,    0,    0,   
                                    0,    0,    0,    0,    0,    0,    0,    0,   
                                ],
                            'K': [ 
                                    0,    0,    0,    0,    0,    0,    0,    0,   
                                    0,    0,    0,    0,    0,    0,    0,    0,   
                                    0,    0,    0,    0,    0,    0,    0,    0,   
                                    0,    0,    0,    0,    0,    0,    0,    0,   
                                    0,    0,    0,    0,    0,    0,    0,    0,   
                                    0,    0,    0,    0,    0,    0,    0,    0,   
                                    0,    0,    0,    0,    0,    0,    0,    0, 
                                    0,    0.5,  0.5,  0.5,  0.5,  0.5,  0.5,  0,  
                                ],
                            'k': [
                                    0,    0.5,  0.5,  0.5,  0.5,  0.5,  0.5,  0,   
                                    0,    0,    0,    0,    0,    0,    0,    0,   
                                    0,    0,    0,    0,    0,    0,    0,    0,   
                                    0,    0,    0,    0,    0,    0,    0,    0,   
                                    0,    0,    0,    0,    0,    0,    0,    0,   
                                    0,    0,    0,    0,    0,    0,    0,    0,   
                                    0,    0,    0,    0,    0,    0,    0,    0,   
                                    0,    0,    0,    0,    0,    0,    0,    0,   
                                ]
                        }


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
