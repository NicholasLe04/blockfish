from bitboard_util import set_bit

EXCLUDE_A_FILE = int("01111111_01111111_01111111_01111111_01111111_01111111_01111111_01111111", 2)
EXCLUDE_H_FILE = int("11111110_11111110_11111110_11111110_11111110_11111110_11111110_11111110", 2)

RANK_4 = int("00000000_00000000_00000000_00000000_11111111_00000000_00000000_00000000", 2)
RANK_5 = int("00000000_00000000_00000000_11111111_00000000_00000000_00000000_00000000", 2)


KNIGHT_ATTACKS = {}

for start_index in range(64):
    KNIGHT_ATTACKS[start_index] = int("00000000_00000000_00000000_00000000_00000000_00000000_00000000_00000000", 2)
    for dir in [17, 15, 10, 6, -6, -10, -15, -17]:
        if 0 <= start_index + dir < 64 and (-2 <= (start_index+dir)//8 - start_index//8 <= 2) and (-2 <= (start_index+dir)%8 - start_index%8 <= 2):
            KNIGHT_ATTACKS[start_index] = set_bit(KNIGHT_ATTACKS[start_index], start_index + dir)