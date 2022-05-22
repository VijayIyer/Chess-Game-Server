import os
import numpy as np
from moves import Move

class piece:
    def __init__(self, color, current_pos):
       if color == 'white':
           self.own, self.oppos = 1, -1
       else:
           self.own, self.oppos = -1, 1
       self.current_pos = current_pos
    def __str__(self):
        return ''
    def get_valid_moves():
        return []
    
       
class pawn(piece):
    def __init__(self, color, current_pos):
        super().__init__(color, current_pos)
        self.has_moved = False

    def __str__(self):
        return ''
    def get_valid_moves(self, board_map):
        row, col = self.current_pos[0], self.current_pos[1]
        moves = []
        
        ## Promoted piece logic left
        ## en passant logic left
        
        if not board_map[row+self.oppos, col] == self.oppos:
            move = self.initialize_pawn_move(board_map)
            move.new_pos = (row+self.oppos, col)
            moves.append(move)
        if not board_map[row+2*self.oppos, col] == self.oppos\
            and not self.has_moved:
            move = self.initialize_pawn_move(board_map)
            move.new_pos = (row+2*self.oppos, col)
            moves.append(move)
        if col+1 < board_map.shape[1]\
            and board_map[row+self.oppos, col+1] == self.oppos:
            move = self.initialize_pawn_move(board_map)
            move.new_pos = (row+self.oppos, col+1)
            move.is_capture = True
            moves.append(move)
            
        if col-1 >= 0\
            and board_map[row+self.oppos, col-1] == self.oppos:
            move = self.initialize_pawn_move(board_map)
            move.new_pos = (row+self.oppos, col-1)
            moves.append(move)
            move.is_capture = True
        return moves
    
    
    def initialize_pawn_move(self, board_map):
        move = Move()
        move.piece_type = pawn
        move.current_pos = self.current_pos
        return move
        
        
        
class rook(piece):
    def __init__(self, color, current_pos):
        super().__init__(color, current_pos)
        self.has_moved = False
    def __str__(self):
        return ('white' if self.own == 1 else 'black') + 'p'
    def get_valid_moves(self, board_map):
        return []
    def initialize_pawn_move(self, board_map):
        move = Move()
        move.piece_type = rook
        move.current_pos = self.current_pos
        return move
    def __str__(self):
        return 'R'
        
class queen(piece):
    def __init__(self, color, current_pos):
        super().__init__(color, current_pos)
        self.has_moved = False
    def __str__(self):
        return ('white' if self.own == 1 else 'black') + 'p'
    def get_valid_moves(self, board_map):
        return []
    def initialize_pawn_move(self, board_map):
        move = Move()
        move.piece_type = rook
        move.current_pos = self.current_pos
        return move
    def __str__(self):
        return 'Q'

class king(piece):
    def __init__(self, color, current_pos):
        super().__init__(color, current_pos)
        self.has_moved = False
    def __str__(self):
        return ('white' if self.own == 1 else 'black') + 'p'
    def get_valid_moves(self, board_map):
        return []
    def initialize_pawn_move(self, board_map):
        move = Move()
        move.piece_type = rook
        move.current_pos = self.current_pos
        return move
    def __str__(self):
        return 'K'

class knight(piece):
    def __init__(self, color, current_pos):
        super().__init__(color, current_pos)
        self.has_moved = False
    def __str__(self):
        return ('white' if self.own == 1 else 'black') + 'p'
    def get_valid_moves(self, board_map):
        return []
    def initialize_pawn_move(self, board_map):
        move = Move()
        move.piece_type = rook
        move.current_pos = self.current_pos
        return move
    def __str__(self):
        return 'N'

class bishop(piece):
    def __init__(self, color, current_pos):
        super().__init__(color, current_pos)
        self.has_moved = False
    def __str__(self):
        return ('white' if self.own == 1 else 'black') + 'p'
    def get_valid_moves(self, board_map):
        return []
    def initialize_pawn_move(self, board_map):
        move = Move()
        move.piece_type = rook
        move.current_pos = self.current_pos
        return move
    def __str__(self):
        return 'B'
        
class king(piece):
    def __init__(self, color, current_pos):
        super().__init__(color, current_pos)
        self.has_moved = False
    def __str__(self):
        return ('white' if self.own == 1 else 'black') + 'p'
    def get_valid_moves(self, board_map):
        return []
    def initialize_pawn_move(self, board_map):
        move = Move()
        move.piece_type = rook
        move.current_pos = self.current_pos
        return move
    def __str__(self):
        return 'K'
        