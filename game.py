import initializations as init
from Piece import pawn, rook, queen, knight, bishop, king
import numpy as np
from moves import Move
import re
import copy
import sys
import json


class Player:
    '''Contains collection of pieces of both sides'''

    def __init__(self, color):
        self.color = color
        self.pieces = []

    def add_piece(self, piece):
        self.pieces.append(piece)


def update_turn(turn):
    return 1 if turn == 0 else 0


def get_possible_moves(cur_pieces, board_map):
    return [piece.get_valid_moves() for piece in cur_pieces]


def infer_move(move_notation, turn):
    '''
    work on this regex
    (?'piece'[K|N|B|R|Q]?)(?'amb'[a-h1-8]?)(?'capture'[x]?)(?'newcol'[a-h]{1})(?'newrow'[1-8]{1})(?'checkormate'[+|#]*)$

    :param move:
    :param color:
    :return:
    '''
    pattern = re.compile('(?P<piece>[K|N|B|R|Q]?)(?P<amb>[a-h1-8]?)(?P<capture>[x]?)(?P<newcol>[a-h]{1})('
                         '?P<newrow>[1-8]{1})(?P<promotion>=([N|B|R|Q]){1})?(?P<checkormate>[+|#]?)$|('
                         '?P<LongCastle>^(O-O-O){1})$|(?P<Castle>^(O-O){1})$')
    m = re.match(pattern=pattern, string=move_notation)
    m_dict = m.groupdict()

    move = Move()
    move.piece_type = pawn
    # region determining piece type
    if m_dict['piece'] != '':
        if m_dict['piece'] == 'R':
            move.piece_type = rook
        elif m_dict['piece'] == 'Q':
            move.piece_type = queen
        elif m_dict['piece'] == 'N':
            move.piece_type = knight
        elif m_dict['piece'] == 'B':
            move.piece_type = bishop
        elif m_dict['piece'] == 'K':
            move.piece_type = king
        else:
            move.piece_type = pawn
    # endregion
    promoted_piece = None
    if m_dict['LongCastle'] is not None:
        move.is_longcastling = True
        if turn == 0:
            move.current_pos = (7, 4)
            move.new_pos = (7, 6)
        elif turn == 1:
            move.current_pos = (0, 4)

            move.new_pos = (0, 6)
    if m_dict['Castle'] is not None:
        move.is_castling = True
        if turn == 0:
            move.current_pos = (7, 4)
            move.new_pos = (7, 2)

        elif turn == 1:
            move.current_pos = (0, 4)
            move.new_pos = (0, 2)

    # region determining prev column
    old_row, old_col = None, None
    if m_dict['amb'] != '':
        if m_dict['amb'] in ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h']:
            old_row = 104 - ord(m_dict['amb'])
        elif m_dict['amb'] in ['1', '2', '3', '4', '5', '6', '7', '8']:
            old_col = int(m_dict['amb']) - 1
        move.current_pos = (old_row, old_col)
    # endregion

    # region determining move type
    if m_dict['capture'] != '':
        move.is_capture = True
    # endregion
    if m_dict['promotion'] is not None:
        move.is_promotion = True
        if m_dict['promotion'][1] == 'Q':
            move.promoted_piece = queen
        if m_dict['promotion'][1] == 'R':
            move.promoted_piece = rook
        if m_dict['promotion'][1] == 'N':
            move.promoted_piece = knight
        if m_dict['promotion'][1] == 'B':
            move.promoted_piece = bishop

    move.new_pos = 8 - int(m_dict['newrow']), 8 - (104 - ord(m_dict['newcol'])) - 1

    return move


def is_move_valid(move, cur_pieces, opp_pieces, board_map):
    is_valid = True
    valid_pieces = cur_pieces
    valid_pieces = [pc for pc in cur_pieces if type(pc) == move.piece_type]
    candidate_moves = []
    selected_move = None
    for piece in cur_pieces:
        possible_moves = piece.get_valid_moves(board_map)
        for possible_move in possible_moves:
            if move == possible_move:
                candidate_moves.append(possible_move)
    if len(candidate_moves) == 1:
        selected_move = move
        selected_move.current_pos = candidate_moves[0].current_pos
    return selected_move


def update_board(move, cur_pieces, opp_pieces, board_map, turn):
    if turn == 0:
        own, oppos = 1, -1
    else:
        own, oppos = -1, 1
    curr_row, curr_col = move.current_pos
    new_row, new_col = move.new_pos
    board_map[curr_row, curr_col] = 0
    board_map[new_row, new_col] = own
    for piece in cur_pieces:
        if piece.current_pos == (curr_row, curr_col):
            piece.current_pos = new_row, new_col
            break
    if move.is_capture:
        for opp_piece in opp_pieces:
            if opp_piece.current_pos == (new_row, new_col):
                opp_pieces.remove(opp_piece)
                break


def create_piece_per_conf(piece_pos):
    piece_row, piece_col = 8 - int(piece_pos[1]), \
                           8 - (104 - ord(piece_pos[0])) - 1
    if piece_pos[3] == "W":
        color = "white"
    else:
        color = "black"
    piece = None
    if piece_pos[4] == "Q":
        piece = queen(color, current_pos=(piece_row, piece_col))
    elif piece_pos[4] == "R":
        piece = rook(color, current_pos=(piece_row, piece_col))
    elif piece_pos[4] == "N":
        piece = knight(color, current_pos=(piece_row, piece_col))
    elif piece_pos[4] == "K":
        piece = king(color, current_pos=(piece_row, piece_col))
    elif piece_pos[4] == "B":
        piece = bishop(color, current_pos=(piece_row, piece_col))
    else:
        piece = pawn(color, current_pos=(piece_row, piece_col))
    return piece

def get_positions(pieces):
    request = dict()
    positions = []
    for piece in pieces:
        pos = ""
        pos += chr(97+piece.current_pos[1])
        pos += str(8 - piece.current_pos[0])
        pos += " "
        pos += ("W" if piece.own == 1 else "B")
        pos += str(piece)
        positions.append(pos)

    return positions

def start_game(board_conf):
    turn = 0
    timer1 = 300
    timer2 = 300
    board_map = np.zeros((8, 8))
    current_game = ""
    move_no = 1
    player1 = Player("white")
    player2 = Player("black")
    pieces = [create_piece_per_conf(line) for line in board_conf]
    for piece in pieces:
        if piece.own == 1:
            player1.add_piece(piece)
            board_map[piece.current_pos[0], piece.current_pos[1]] = 1

        else:
            player2.add_piece(piece)
            board_map[piece.current_pos[0], piece.current_pos[1]] = -1

    while True:
        if turn == 0:
            cur_pieces = player1.pieces
            opp_pieces = player2.pieces

            # next turn in notational terms
            current_game += " {}.".format(move_no)
            move_no += 1

        elif turn == 1:
            cur_pieces = player2.pieces
            opp_pieces = player1.pieces

        move_notation = input("\nenter your move:")
        move = infer_move(move_notation, turn)
        selected_move = is_move_valid(move, cur_pieces, opp_pieces, board_map)
        if selected_move is not None:
            current_game += move_notation + " "
            update_board(move, cur_pieces, opp_pieces, board_map, turn)
            request = json.dumps(get_positions(cur_pieces + opp_pieces))
        else:
            print('\n ---- invalid move ----')
        turn = update_turn(turn)

        option = input("\ndo you want to continue? [y/n]")
        if (option != "y"): break
    print(current_game)
    print(board_map)


if __name__ == "__main__":
    print(sys.argv[1])
    board_conf_file = sys.argv[1]
    with open(board_conf_file, 'r') as f:
        board_conf = f.readlines()
    start_game(board_conf)
