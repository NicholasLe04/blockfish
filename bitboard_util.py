import math

def get_bit(bitboard, position):
    return (bitboard >> position) & 1

def set_bit(bitboard, position):
    return bitboard | (1 << position)

def clear_bit(bitboard, position):
    return bitboard & ~(1 << position)

def bitboard_to_board(bitboard:str):
    bitboard = bitboard[2:]
    while len(bitboard) < 64:
        bitboard = '0' + bitboard

    for i in range(0, 64, 8):
        print(bitboard[i:i+8])

def index_of_LSB(bitboard):
    return (bitboard&-bitboard).bit_length()-1

def index_of_MSB(bitboard):
    return int(math.log2(bitboard))