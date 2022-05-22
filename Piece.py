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
        return 'white' if self.own == 1 else 'black'
    def get_valid_moves():
        return []
       
class pawn(piece):
    def __init__(self, color, current_pos):
        super().__init__(color, current_pos)
        self.has_moved = False
    def __str__(self):
        return ('white' if self.own == 1 else 'black') + 'p'
    def get_valid_moves(self, board_map):
        row, col = self.current_pos[0], self.current_pos[1]
        moves = []
        if not board_map[row+1, col] == self.oppos:
            moves += (row+1, col)
        if not board_map[row+2, col] == self.oppos:
            moves += (row+2, col)
        if board_map[row+1, col+1] == self.oppos:
            moves += (row+1, col+1)
        if board_map[row+1, col-1] == self.oppos:
            moves += (row+1, col-1)
        return [Move(self, move) for move in moves]
        
        


