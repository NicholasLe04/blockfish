
POSITION_MAPPING = {
       26:  'a8',  27: 'b8',    28: 'c8',  29: 'd8',  30: 'e8',  31: 'f8',  32: 'g8',  33: 'h8',
       38:  'a7',  39: 'b7',    40: 'c7',  41: 'd7',  42: 'e7',  43: 'f7',  44: 'g7',  45: 'h7',
       50:  'a6',  51: 'b6',    52: 'c6',  53: 'd6',  54: 'e6',  55: 'f6',  56: 'g6',  57: 'h6',
       62:  'a5',  63: 'b5',    64: 'c5',  65: 'd5',  66: 'e5',  67: 'f5',  68: 'g5',  69: 'h5',
       74:  'a4',  75: 'b4',    76: 'c4',  77: 'd4',  78: 'e4',  79: 'f4',  80: 'g4',  81: 'h4',
       86:  'a3',  87: 'b3',    88: 'c3',  89: 'd3',  90: 'e3',  91: 'f3',  92: 'g3',  93: 'h3',
       98:  'a2',  99: 'b2',   100: 'c2', 101: 'd2', 102: 'e2', 103: 'f2', 104: 'g2', 105: 'h2',
       110: 'a1', 111: 'b1',   112: 'c1', 113: 'd1', 114: 'e1', 115: 'f1', 116: 'g1', 117: 'h1',
   }

class Move():

    def __init__(self, **kwargs) -> None:
        '''
        Standard Move -> Move(type='standard', capture=True/False, start=*start_index*, end=*end_index*)\n
        Capture Move -> Move(type='capture', start=*start_index*, end=*end_index*)\n
        En Passant -> Move(type='en passant', start=*start_index*, ep_idx=*index of final position of capturing pawn*)\n
        Castle Move -> Move(type='castle', castle_side='K'/'Q')
        Pawn First Move -> Move(type='first pawn', start=*start_index*, end=*end_index*, ep_idx=*square vulnerable for ep*)\n
        Promotion -> Move(type='promotion', start=*start_index*, end=*end_index*, new_piece=*N/B/R/Q*)
        '''
        # Ensure type arg exists
        if 'type' not in kwargs:
            raise Exception("Move needs a type")
        else:
            self.type = kwargs['type']


        if self.type == "standard":
            self.start_idx = kwargs['start']
            self.end_idx = kwargs['end']
        elif self.type == "capture":
            self.start_idx = kwargs['start']
            self.end_idx = kwargs['end']
        elif self.type == "en passant":
            self.start_idx = kwargs['start']
            self.end_idx = kwargs['end']
            self.ep_idx = kwargs['ep_idx']
        elif self.type == "castle":
            self.castle_side = kwargs['castle_side']
        elif self.type == "first pawn":
            self.start_idx = kwargs['start']
            self.end_idx = kwargs['end'] 
            self.ep_idx = kwargs['ep_idx']
        elif self.type == "promotion":
            self.start_idx = kwargs['start']
            self.end_idx = kwargs['end'] 
            self.new_piece = kwargs['new_piece']
        else:
            raise Exception("really ninja")
    
    def __str__(self):
        if self.type == 'castle':
            return "O-O-O" if self.castle_side ==  "Q" else "O-O"
        else:
            notated_move = POSITION_MAPPING[self.start_idx]+POSITION_MAPPING[self.end_idx]
            return notated_move + self.new_piece if self.type == 'promotion' else notated_move
            
        
        
    def __repr__(self) -> str:
        return self.__str__()