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
    if bitboard == 0:
        return -2
    return int(math.log2(bitboard))

def bitscan(bitboard):
    '''
        Return a list with the index of every 1-bit from the right\n
        bitboard: 001100011010111
        bitscan(bitboard) -> [0,1,2,4,6,7,11,12]
    '''
    indices = []
    for i in range(index_of_LSB(bitboard), index_of_MSB(bitboard)+1):
        if get_bit(bitboard, i):
            indices.append(i)

    return indices