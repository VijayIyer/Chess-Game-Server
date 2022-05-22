class Move:
    def __init__(self, notation):
        self.notation = notation 
        self.current_pos = None
        self.next_pos = None
        self.piece, self.current_pos, self.next_pos = infer_move(notation)

    
