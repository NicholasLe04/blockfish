import pieces.bishop as bishop
import pieces.rook as rook

def queen_attacks(start_index, all_pieces):
    return ( 
            bishop.bishop_attacks(start_index, all_pieces) | 
            rook.rook_attacks(start_index, all_pieces) 
        )

def queen_moves(start_index, friendly_pieces, all_pieces):
    return queen_attacks(start_index, all_pieces) & ~friendly_pieces