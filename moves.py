class Move:
    def __init__(self):
        self.piece_type = None
        self.is_castling = False
        self.is_longcastling = False
        self.new_pos = None
        self.current_pos = None
        self.is_promotion = False
        self.promoted_piece = None
        self.is_enpassant = False
        self.is_capture = False
    def __eq__(self, other):
        ans = True
        if (isinstance(other, Move)):
            ans = ans & (self.piece_type == other.piece_type)
            ans = ans & (self.is_castling == other.is_castling)
            ans = ans & (self.is_longcastling == other.is_longcastling)
            ans = ans & (self.new_pos == other.new_pos)
            #print(self.current_pos, other.current_pos)
            if self.current_pos != (None, None):
                if self.current_pos[0] is not None:
                    if self.current_pos[0] != other.current_pos[0]:
                        #print('returning1')
                        return False
                if self.current_pos[1] is not None:
                    if self.current_pos[1] != other.current_pos[1]:
                        #print('returning2')
                        return False
            #ans = ans & (self.current_pos == other.current_pos)
            ans = ans & (self.is_promotion == other.is_promotion)
            ans = ans & (self.promoted_piece == other.promoted_piece)
            # ans = ans & (self.is_enpassant == other.is_enpassant)
            ans = ans & (self.is_capture == other.is_capture)
        return ans
