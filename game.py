import initializations as init
from typing import List, Tuple
from Piece import pawn, rook, queen, knight, bishop, king
import numpy as np
from moves import Move
import re
import copy
import sys
import json
import logging

# logging.basicConfig(filename='test.log',level=logging.DEBUG)
timer1 = 300  # 5 minutes
timer2 = 300  # 5 minutes


class Player:
    """Contains collection of pieces of both sides"""

    def __init__(self, color):
        self.color = color
        self.pieces = []
        self.in_check = False
        self.in_checkmate = False

    def add_piece(self, piece):
        self.pieces.append(piece)


def get_possible_moves(cur_pieces, board_map):
    return [piece.get_valid_moves() for piece in cur_pieces]


def infer_move(move_notation: str, turn: int) -> Move:
    '''
    work on this regex
    (?'piece'[K|N|B|R|Q]?)(?'amb'[a-h1-8]?)(?'capture'[x]?)(?'newcol'[a-h]{1})(?'newrow'[1-8]{1})(?'checkormate'[+|#]*)$

    :param move_notation: the move to be performed in valid chess string format
    :param turn: integer denoting whether the player performing the move is white or black
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

        move.piece_type = king
        move.is_castling = True
        if turn == 0:
            move.current_pos = (7, 4)
            move.new_pos = (7, 6)

            return move

        elif turn == 1:
            move.current_pos = (0, 4)
            move.new_pos = (0, 6)

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


def create_piece_per_conf(piece_pos):
    """
    Creates piece based on notation. e.g. Wp is a white pawn, WB is a white bishop
    """
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
    """
    returns a list of strings with each string in the form of the configuration used to create the board
     e.g. a1 Wp is white pawn on a1 square
    """
    positions = []
    for piece in pieces:
        pos = ""
        pos += chr(97 + piece.current_pos[1])
        pos += str(8 - piece.current_pos[0])
        pos += " "
        pos += ("W" if piece.own == 1 else "B")
        pos += str(piece)
        positions.append(pos)
    return positions


class Game:
    def __init__(self, game_id: int):
        self.id = game_id
        self.player1 = Player("white")
        self.player2 = Player("black")
        self.board_map = np.zeros((8, 8))
        self.turn = 0
        self.move_no = 1
        self.current_game = ""
        self.is_invalid_move = False
        self.over = False

    def initialize_players(self, board_conf):
        pieces = [create_piece_per_conf(line) for line in board_conf]
        for piece in pieces:
            if piece.own == 1:
                self.player1.add_piece(piece)
                self.board_map[piece.current_pos[0], piece.current_pos[1]] = 1

            else:
                self.player2.add_piece(piece)
                self.board_map[piece.current_pos[0], piece.current_pos[1]] = -1

    @staticmethod
    def get_king_pos(player: Player) -> Tuple[int, int]:

        for pc in player.pieces:
            if type(pc) == king:
                return pc.current_pos
        else:
            if player.color == 'white':
                return 7, 4  # default white king pos
            else:
                return 0, 4

    def update_turn(self):
        return 1 if self.turn == 0 else 0

    def get_squares_under_attack(self, player: Player) -> List[Tuple[int, int]]:
        squares_under_attack: List[Tuple[int, int]] = []
        for pc in player.pieces:
            if isinstance(pc, pawn):
                for mv in pc.get_valid_moves(self.board_map):
                    if mv.is_capture:
                        squares_under_attack.append(mv.new_pos)
            else:
                for mv in pc.get_valid_moves(self.board_map):
                    if mv.new_pos not in squares_under_attack:
                        squares_under_attack.append(mv.new_pos)
        return squares_under_attack

    def is_enpassant_valid(self, possible_move, opp_pieces):
        cur_row, cur_col = possible_move.current_pos[0], possible_move.current_pos[1]
        if self.board_map[cur_row, cur_col] == 1:
            own = 1
            oppos = -1
        else:
            own = -1
            oppos = 1
        new_row, new_col = possible_move.new_pos[0], possible_move.new_pos[1]
        # logging.debug("checking for {},{} to be captured".format(new_row, new_col))
        if self.board_map[cur_row, new_col] != oppos:
            return False
        piece_to_be_captured = None
        for piece in opp_pieces:
            if piece.current_pos == (cur_row, new_col):
                piece_to_be_captured = piece
                break
        if piece_to_be_captured is None:
            return False
        return piece_to_be_captured.can_be_enpassanted

    def is_castling_valid(self, move, cur_player: Player, opp_player: Player) -> bool:
        cur_pieces = cur_player.pieces
        opp_pieces = opp_player.pieces
        cur_king = list(filter(lambda pc: type(pc) == king, cur_pieces))[0]
        rooks = list(filter(lambda pc: type(pc) == rook, cur_pieces))
        cur_rook = list(filter(lambda pc: pc.current_pos == (cur_king.current_pos[0],
                                                             cur_king.current_pos[1] + 3),
                               rooks))[0]
        if cur_king.has_moved:
            return False
        if cur_rook.has_moved:
            return False
        if self.board_map[move.current_pos[0], move.current_pos[1] + 1] != 0 \
                or self.board_map[move.current_pos[0], move.current_pos[1] + 2] != 0:
            return False

        castling_squares = [(move.current_pos[0], move.current_pos[1]),
                            (move.current_pos[0], move.current_pos[1] + 1),
                            (move.current_pos[0], move.current_pos[1] + 2)]
        squares_under_attack = self.get_squares_under_attack(opp_player)
        if any(x in squares_under_attack for x in castling_squares):
            return False
        return True

    def is_longcastling_valid(self, move: Move, cur_player: Player, opp_player: Player) -> bool:
        cur_pieces = cur_player.pieces
        opp_pieces = opp_player.pieces
        cur_king = list(filter(lambda pc: type(pc) == king, cur_pieces))[0]
        rooks = list(filter(lambda pc: type(pc) == rook, cur_pieces))
        cur_rook = list(filter(lambda pc: pc.current_pos == (cur_king.current_pos[0],
                                                             cur_king.current_pos[1] - 4),
                               rooks))[0]
        if cur_king.has_moved:
            return False
        if cur_rook.has_moved:
            return False
        if self.board_map[move.current_pos[0], move.current_pos[1] - 1] != 0 \
                or self.board_map[move.current_pos[0], move.current_pos[1] - 2] != 0 \
                or self.board_map[move.current_pos[0], move.current_pos[1] - 3] != 0:
            return False
        squares_under_attack = self.get_squares_under_attack(opp_player)

        castling_squares = [(move.current_pos[0], move.current_pos[1]),
                            (move.current_pos[0], move.current_pos[1] - 1),
                            (move.current_pos[0], move.current_pos[1] - 2),
                            (move.current_pos[0], move.current_pos[1] - 3)]
        if any(x in squares_under_attack for x in castling_squares):
            return False
        return True

    def is_king_move_valid(self, move: Move, opp_player: Player) -> bool:
        squares_under_attack = self.get_squares_under_attack(opp_player)
        if move.new_pos in squares_under_attack:
            return False
        return True

    def get_valid_move(self, move: Move, cur_player: Player, opp_player: Player) -> Move or None:
        # change 'type' call to selection logic
        cur_pieces = cur_player.pieces
        opp_pieces = opp_player.pieces
        valid_pieces = [pc for pc in cur_pieces if isinstance(pc, move.piece_type)]
        candidate_moves = []
        for piece in valid_pieces:

            # checking if the move is equal to any of the possible moves
            possible_moves = piece.get_valid_moves(self.board_map)

            for possible_move in possible_moves:
                if isinstance(piece, king) and not self.is_king_move_valid(move, opp_player):
                    continue
                if move == possible_move:

                    if possible_move.is_enpassant:
                        if not self.is_enpassant_valid(possible_move, opp_pieces):
                            continue
                    if possible_move.is_castling:
                        if not self.is_castling_valid(possible_move, cur_player, opp_player):
                            continue
                    if possible_move.is_longcastling:
                        if not self.is_longcastling_valid(possible_move, cur_player, opp_player):
                            continue
                    candidate_moves.append(possible_move)

        # if no ambiguity
        if len(candidate_moves) == 1:
            selected_move = move
            selected_move.current_pos = candidate_moves[0].current_pos
            if candidate_moves[0].is_enpassant:
                selected_move.is_enpassant = True
            return selected_move
        else:
            return None

    def update_board(self, move, cur_pieces, opp_pieces):
        print("updated board called")
        if self.turn == 0:
            own, oppos = 1, -1
        else:
            own, oppos = -1, 1
        curr_row, curr_col = move.current_pos
        new_row, new_col = move.new_pos
        self.board_map[curr_row, curr_col] = 0
        self.board_map[new_row, new_col] = own
        for piece in cur_pieces:
            if piece.current_pos == (curr_row, curr_col):
                piece.current_pos = new_row, new_col
                if type(piece) == pawn and not piece.has_moved \
                        and move.new_pos == (curr_row + 2 * oppos, curr_col):
                    piece.can_be_enpassanted = True

                piece.has_moved = True
            elif type(piece) == pawn:
                piece.can_be_enpassanted = False
        if move.is_castling:

            for piece in cur_pieces:
                if type(piece) == rook:
                    print('{}:{}'.format((new_row, new_col), piece.current_pos))
                    if piece.current_pos == (curr_row, curr_col + 3):
                        piece.current_pos = new_row, new_col - 1
                        break
        if move.is_longcastling:

            for piece in cur_pieces:
                if type(piece) == rook:
                    print('{}:{}'.format((new_row, new_col), piece.current_pos))
                    if piece.current_pos == (curr_row, curr_col - 4):
                        piece.current_pos = new_row, new_col + 1
                        break
        if move.is_capture:
            for opp_piece in opp_pieces:
                if move.is_enpassant:

                    if opp_piece.current_pos == (new_row - oppos, new_col):
                        opp_pieces.remove(opp_piece)
                        break
                if opp_piece.current_pos == (new_row, new_col):
                    opp_pieces.remove(opp_piece)
                    break

    def check_king_in_check(self, move: Move, turn: int):
        possible_game = copy.deepcopy(self)
        possible_game.turn = turn
        if possible_game.turn == 0:
            cur_player = possible_game.player1
            opp_player = possible_game.player2
        elif possible_game.turn == 1:
            cur_player = possible_game.player2
            opp_player = possible_game.player1
        else:
            return False
        possible_game.update_board(move, cur_player.pieces, opp_player.pieces)
        curr_king_pos = possible_game.get_king_pos(cur_player)
        opp_squares_under_attack = possible_game.get_squares_under_attack(opp_player)
        if curr_king_pos in opp_squares_under_attack:
            print("invalid move since it puts self in check")
            print('king is currently at {}'.format(curr_king_pos))
            print('squares under attack: {}'.format(opp_squares_under_attack))
            # revert board here
            return True
        else:
            return False

    def make_move(self, move_notation):
        # switch players based on turn
        if self.turn == 0:
            current_player = self.player1
            opp_player = self.player2

        else:
            current_player = self.player2
            opp_player = self.player1
        # move_notation = input("\nenter your move:")
        move = infer_move(move_notation, self.turn)
        selected_move = self.get_valid_move(move, current_player, opp_player)

        # if move is valid, take action
        if selected_move is not None and not self.check_king_in_check(selected_move, self.turn):
            # actual board update
            self.update_board(selected_move, current_player.pieces, opp_player.pieces)
            # recording if king is in check
            cur_squares_under_attack = self.get_squares_under_attack(current_player)
            opp_king_pos = self.get_king_pos(opp_player)
            if opp_king_pos in cur_squares_under_attack:
                # check for checkmate
                opp_king: king = [piece for piece in opp_player.pieces if isinstance(piece, king)][0]
                if all(self.check_king_in_check(move, 1 if self.turn == 0 else 0)
                       for move in opp_king.get_valid_moves(self.board_map)):
                    self.over = True
                opp_player.in_check = True
                print("{} is in check".format(opp_player.color))
            else:
                opp_player.in_check = False
            self.turn = self.update_turn()
            self.is_invalid_move = False
            if self.turn == 1:
                # next turn in notational terms
                self.current_game += " {}.".format(self.move_no)
                self.move_no += 1
            self.current_game += move_notation + ("+" if opp_player.in_check else "") + " "
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
