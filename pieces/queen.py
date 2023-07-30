import pieces.bishop as bishop
import pieces.rook as rook

def queen_moves(start_index, all_pieces):
    return ( 
            bishop.bishop_attacks(start_index, all_pieces) | 
            rook.rook_attacks(start_index, all_pieces) 
        )
