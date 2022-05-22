import os
from Piece import piece, pawn

def initialize_pieces(color):
    pieces = []
    pieces.append(initialize_pawns(color))
    return pieces

def initialize_pawns(color):
    white_pos = [(6, 0), (6, 1), (6, 2), (6, 3), (6, 4), (6, 5), (6, 6), (6, 7)]
    black_pos = [(0, 0), (0, 1), (0, 2), (0, 3), (0, 4), (0, 5), (0, 6), (0, 7)]
    if color == "white":
        return [pawn(color, pos) for pos in white_pos]
    elif color == "black":
        return [pawn(color, pos) for pos in black_pos]
    
