import initializations as init
from Piece import pawn, rook, queen, knight, bishop, king
import numpy as np
from moves import Move
import re
import copy
import sys
import json
import logging

# logging.basicConfig(filename='test.log',level=logging.DEBUG)
turn = 0
timer1 = 300 #5 minutes
timer2 = 300 #5 minutes


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
        print('long castle')
        move.is_longcastling = True
        move.piece_type = king
        if turn == 0:

            move.current_pos = (7, 4)
            move.new_pos = (7, 1)
            return move
        elif turn == 1:
            move.current_pos = (0, 4)
            move.new_pos = (0, 1)
            return move

    if m_dict['Castle'] is not None:
        # print('castling move')
        move.piece_type = king
        move.is_castling = True
        if turn == 0:
            move.current_pos = (7, 4)
            move.new_pos = (7, 6)
            # print('{}:{}'.format(move.current_pos, move.new_pos))
            return move

        elif turn == 1:
            move.current_pos = (0, 4)
            move.new_pos = (0, 6)
            # print('{}:{}'.format(move.current_pos , move.new_pos))
            return move

    # region determining prev column
    move.current_pos = (None, None)
    old_row, old_col = None, None
    if m_dict['amb'] != '':
        if m_dict['amb'] in ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h']:
            old_col = 8 - (104 - ord(m_dict['amb'])) - 1
        elif m_dict['amb'] in ['1', '2', '3', '4', '5', '6', '7', '8']:
            old_row = 8 - int(m_dict['amb'])
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
    # logging.debug('{} to move from {} to {}'.format(move.piece_type, move.current_pos, move.new_pos))
    return move


def is_enpassant_valid(possible_move, opp_pieces, board_map):
    cur_row, cur_col = possible_move.current_pos[0], possible_move.current_pos[1]
    if board_map[cur_row, cur_col] == 1:
        own = 1
        oppos = -1
    else:
        own = -1
        oppos = 1
    new_row, new_col = possible_move.new_pos[0], possible_move.new_pos[1]
    # logging.debug("checking for {},{} to be captured".format(new_row, new_col))
    if board_map[cur_row, new_col] != oppos:
        return False
    piece_to_be_captured = None
    for piece in opp_pieces:
        if piece.current_pos == (cur_row, new_col):
            piece_to_be_captured = piece
            break
    if piece_to_be_captured is None: return False
    return piece_to_be_captured.can_be_enpassanted


def is_move_valid(move, cur_pieces, opp_pieces, board_map):
    is_valid = True
    valid_pieces = [pc for pc in cur_pieces if type(pc) == move.piece_type]
    candidate_moves = []
    for piece in valid_pieces:

        # checking if the move is equal to any of the possible moves
        possible_moves = piece.get_valid_moves(board_map)

        for possible_move in possible_moves:
            #print('{}:{}'.format(possible_move.current_pos, possible_move.new_pos))
            if possible_move.is_enpassant:
                #    print("checking en_passant...")
                if not is_enpassant_valid(possible_move, opp_pieces, board_map):
                    #        print("exiting en_passant check")
                    continue

            if move == possible_move:
                # print(move.current_pos)
                candidate_moves.append(possible_move)
    #  for move in candidate_moves:
    # logging.debug('{}'.format(move.new_pos))
    if len(candidate_moves) == 1:
        selected_move = move
        selected_move.current_pos = candidate_moves[0].current_pos
        if candidate_moves[0].is_enpassant:
            selected_move.is_enpassant = True
        return selected_move
    else:
        # logging.debug('these are the final candidate moves')
        # for move in candidate_moves:
        # logging.debug(move.current_pos, move.new_pos)
        return None


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
            if type(piece) == pawn and not piece.has_moved \
                    and move.new_pos == (curr_row + 2 * oppos, curr_col):
                piece.can_be_enpassanted = True
                # print("{}: {},{} can be en_passanted".format(own, new_row, new_col))
            piece.has_moved = True
        elif type(piece) == pawn:
            piece.can_be_enpassanted = False
    if move.is_capture:
        for opp_piece in opp_pieces:
            if move.is_enpassant:
                # print("this move is en passant")
                if opp_piece.current_pos == (new_row - oppos, new_col):
                    opp_pieces.remove(opp_piece)
                    break
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
    print(len(pieces))
    request = dict()
    positions = []
    for piece in pieces:
        pos = ""
        pos += chr(97 + piece.current_pos[1])
        pos += str(8 - piece.current_pos[0])
        pos += " "
        pos += ("W" if piece.own == 1 else "B")
        pos += str(piece)
        positions.append(pos)
    print(positions)
    return positions


def get_king_pos(pieces):
    for pc in pieces:
        if type(pc) == king:
            return pc.current_pos

    return (7, 4) # default white king pos


class Game:
    def __init__(self):
        self.player1 = Player("white")
        self.player2 = Player("black")
        self.board_map = np.zeros((8, 8))
        self.turn = 0
        self.move_no = 1
        self.current_game = ""
        self.is_invalid_move = False

    def initialize_players(self, board_conf):
        pieces = [create_piece_per_conf(line) for line in board_conf]
        for piece in pieces:
            if piece.own == 1:
                self.player1.add_piece(piece)
                self.board_map[piece.current_pos[0], piece.current_pos[1]] = 1

            else:
                self.player2.add_piece(piece)
                self.board_map[piece.current_pos[0], piece.current_pos[1]] = -1

    def get_squares_under_attack(self, valid_pieces):
        squares_under_attack = []
        for pc in valid_pieces:
            for mv in pc.get_valid_moves(self.board_map):
                if mv.new_pos not in squares_under_attack:
                    squares_under_attack.append(mv.new_pos)
        return squares_under_attack

    def make_move(self, move_notation):
        if self.turn == 0:
            cur_pieces = self.player1.pieces
            opp_pieces = self.player2.pieces
            current_player = self.player1
            opp_player = self.player2

        elif self.turn == 1:
            cur_pieces = self.player2.pieces
            opp_pieces = self.player1.pieces
            current_player = self.player2
            opp_player = self.player1
        # move_notation = input("\nenter your move:")
        move = infer_move(move_notation, self.turn)
        selected_move = is_move_valid(move, cur_pieces, opp_pieces, self.board_map)

        if selected_move is not None:

            update_board(selected_move, cur_pieces, opp_pieces, self.board_map, self.turn)
            cur_squares_under_attack = self.get_squares_under_attack(cur_pieces)
            opp_squares_under_attack = self.get_squares_under_attack(opp_pieces)
            opp_king_pos = get_king_pos(opp_pieces)
            curr_king_pos = get_king_pos(cur_pieces)
            if opp_king_pos in cur_squares_under_attack:
                opp_player.in_check = True
                print("{} is in check".format(opp_player.color))
            if curr_king_pos in opp_squares_under_attack:
                print("invalid move since it puts self in check")
                self.is_invalid_move = True
                # revert board here
                return
            self.turn = update_turn(self.turn)
            self.is_invalid_move = False
            if self.turn == 1:
                # next turn in notational terms
                self.current_game += " {}.".format(self.move_no)
                self.move_no += 1
            self.current_game += move_notation + " "
        else:
            print("move invalid")
            self.is_invalid_move = True

    def get_status(self):
        if self.is_invalid_move:
            return "invalid move"

        return self.current_game

    def get_board(self):
        return self.board_map

    def get_positions(self):
        return get_positions(self.player1.pieces + self.player2.pieces)


class Player:
    """Contains collection of pieces of both sides"""

    def __init__(self, color):
        self.color = color
        self.pieces = []
        self.in_check = False

    def add_piece(self, piece):
        self.pieces.append(piece)


# def start_game(player1, player2, board_map):
#
#
#     while True:
#         if turn == 0:
#             cur_pieces = player1.pieces
#             opp_pieces = player2.pieces
#
#             # next turn in notational terms
#             current_game += " {}.".format(move_no)
#             move_no += 1
#
#         elif turn == 1:
#             cur_pieces = player2.pieces
#             opp_pieces = player1.pieces
#
#         move_notation = input("\nenter your move:")
#         move = infer_move(move_notation, turn)
#         selected_move = is_move_valid(move, cur_pieces, opp_pieces, board_map)
#         print('move selected')
#         if selected_move is not None:
#             current_game += move_notation + " "
#             update_board(move, cur_pieces, opp_pieces, board_map, turn)
#             request = json.dumps(get_positions(cur_pieces + opp_pieces))
#         else:
#             print('\n ---- invalid move ----')
#         turn = update_turn(turn)
#
#         option = input("\ndo you want to continue? [y/n]")
#         if (option != "y"): break
#     print(current_game)
#     print(board_map)


# def initialize_players(board_conf):
#     player1 = Player("white")
#     player2 = Player("black")
#     board_map = np.zeros((8, 8))
#     pieces = [create_piece_per_conf(line) for line in board_conf]
#     for piece in pieces:
#         if piece.own == 1:
#             player1.add_piece(piece)
#             board_map[piece.current_pos[0], piece.current_pos[1]] = 1
#
#         else:
#             player2.add_piece(piece)
#             board_map[piece.current_pos[0], piece.current_pos[1]] = -1
#     return player1, player2, board_map


if __name__ == "__main__":
    pass
    # print(sys.argv[1])
    # board_conf_file = sys.argv[1]
    # with open(board_conf_file, 'r') as f:
    #    board_conf = f.readlines()
    # player1, player2, board_map = initialize_players(board_conf)
    # start_game(player1, player2, board_map)
