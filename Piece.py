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

    def get_valid_moves(self, board_map):
        return []


class pawn(piece):
    def __init__(self, color, current_pos):
        super().__init__(color, current_pos)
        self.has_moved = False
        self.can_be_enpassanted = False

    def __str__(self):
        return 'p'

    def get_valid_moves(self, board_map):
        row, col = self.current_pos[0], self.current_pos[1]
        moves = []

        ## Promoted piece logic left

        if not board_map[row + self.oppos, col] == self.oppos:
            move = self.initialize_pawn_move(board_map)
            move.new_pos = (row + self.oppos, col)
            moves.append(move)
        if not board_map[row + 2 * self.oppos, col] == self.oppos \
                and not self.has_moved:
            move = self.initialize_pawn_move(board_map)
            move.new_pos = (row + 2 * self.oppos, col)
            moves.append(move)
        if col + 1 < board_map.shape[1] \
                and (board_map[row + self.oppos, col + 1] == self.oppos
                     or board_map[row, col + 1] == self.oppos):
            move = self.initialize_pawn_move(board_map)
            move.new_pos = (row + self.oppos, col + 1)
            move.is_capture = True
            if board_map[row, col + 1] == self.oppos:
                move.is_enpassant = True
            moves.append(move)

        if col - 1 >= 0 \
                and (board_map[row + self.oppos, col - 1] == self.oppos \
                     or board_map[row, col - 1] == self.oppos):
            move = self.initialize_pawn_move(board_map)
            move.new_pos = (row + self.oppos, col - 1)

            move.is_capture = True
            if board_map[row, col - 1] == self.oppos:
                # print("en_passant move an option...for {}:{},{}".format(self.own, row, col))
                move.is_enpassant = True
            moves.append(move)
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

    def get_valid_moves(self, board_map):
        row, col = self.current_pos[0], self.current_pos[1]
        moves = []
        i = 1
        while col + i < board_map.shape[1]:
            if board_map[row, col + i] != self.own:
                move = self.add_move(board_map, (row, col + i))
                if move is not None:
                    moves.append(move)
                if board_map[row, col + i] == self.oppos:
                    break
                i += 1
            else:
                break
        i = 1
        while col - i >= 0:
            if board_map[row, col - i] != self.own:
                move = self.add_move(board_map, (row, col - i))
                if move is not None:
                    moves.append(move)
                if board_map[row, col - i] == self.oppos:
                    break
                i += 1
            else:
                break
        i = 1
        while row + i < board_map.shape[0]:
            if board_map[row + i, col] != self.own:
                move = self.add_move(board_map, (row + i, col))
                if move is not None:
                    moves.append(move)
                if board_map[row + i, col] == self.oppos:
                    break
                i += 1

            else:
                break
        i = 1
        while row - i >= 0:
            if board_map[row - i, col] != self.own:
                move = self.add_move(board_map, (row - i, col))
                if move is not None:
                    moves.append(move)
                if board_map[row - i, col] == self.oppos:
                    break
                i += 1
            else:
                break

        return moves

    def initialize_rook_move(self, board_map):
        move = Move()
        move.piece_type = rook
        move.current_pos = self.current_pos
        return move

    def add_move(self, board_map, new_pos):
        row, col = new_pos[0], new_pos[1]
        if (0 <= row < board_map.shape[0]) and (0 <= col < board_map.shape[1]) \
                and board_map[row, col] != self.own:
            move = self.initialize_rook_move(board_map)
            move.new_pos = (row, col)
            if board_map[row, col] == self.oppos:
                move.is_capture = True

            return move
        else:
            return None

    def __str__(self):
        return 'R'


class queen(piece):
    def __init__(self, color, current_pos):
        super().__init__(color, current_pos)
        self.has_moved = False

    def get_valid_moves(self, board_map):
        row, col = self.current_pos[0], self.current_pos[1]

        moves = []

        i = 1
        while col + i < board_map.shape[1] and row + i < board_map.shape[0]:
            if board_map[row + i, col + i] != self.own:
                move = self.add_move(board_map, (row + i, col + i))
                if move is not None:
                    moves.append(move)
                if board_map[row + i, col + i] == self.oppos:
                    break
                i += 1
            else:
                break
        i = 1
        while col - i >= 0 and row + i < board_map.shape[0]:
            if board_map[row + i, col - i] != self.own:
                move = self.add_move(board_map, (row + i, col - i))
                if move is not None:
                    moves.append(move)
                if board_map[row + i, col - i] == self.oppos:
                    break
                i += 1
            else:
                break
        i = 1
        while row - i > 0 and col - i > 0:
            if board_map[row - i, col - i] != self.own:
                move = self.add_move(board_map, (row - i, col - i))
                if move is not None:
                    moves.append(move)
                if board_map[row - i, col - i] == self.oppos:
                    break
                i += 1

            else:
                break
        i = 1
        while row - i >= 0 and col + i < board_map.shape[1]:
            if board_map[row - i, col + i] != self.own:
                move = self.add_move(board_map, (row - i, col + i))
                if move is not None:
                    moves.append(move)
                if board_map[row - i, col + i] == self.oppos:
                    break
                i += 1
            else:
                break
        i = 1
        while col + i < board_map.shape[1]:
            if board_map[row, col + i] != self.own:
                move = self.add_move(board_map, (row, col + i))
                if move is not None:
                    moves.append(move)
                if board_map[row, col + i] == self.oppos:
                    break
                i += 1
            else:
                break
        i = 1
        while col - i >= 0:
            if board_map[row, col - i] != self.own:
                move = self.add_move(board_map, (row, col - i))
                if move is not None:
                    moves.append(move)
                if board_map[row, col - i] == self.oppos:
                    break
                i += 1
            else:
                break
        i = 1
        while row + i < board_map.shape[0]:
            if board_map[row + i, col] != self.own:
                move = self.add_move(board_map, (row + i, col))
                if move is not None:
                    moves.append(move)
                if board_map[row + i, col] == self.oppos:
                    break
                i += 1

            else:
                break
        i = 1
        while row - i >= 0:
            if board_map[row - i, col] != self.own:
                move = self.add_move(board_map, (row - i, col))
                if move is not None:
                    moves.append(move)
                if board_map[row - i, col] == self.oppos:
                    break
                i += 1
            else:
                break


        return moves

    def add_move(self, board_map, new_pos):
        row, col = new_pos[0], new_pos[1]
        if (0 <= row < board_map.shape[0]) and (0 <= col < board_map.shape[1]) \
                and board_map[row, col] != self.own:
            move = self.initialize_queen_move(board_map)
            move.new_pos = (row, col)
            if board_map[row, col] == self.oppos:
                move.is_capture = True

            return move
        else:
            return None

    def initialize_queen_move(self, board_map):
        move = Move()
        move.piece_type = queen
        move.current_pos = self.current_pos
        return move

    def __str__(self):
        return 'Q'


class king(piece):
    def __init__(self, color, current_pos):
        super().__init__(color, current_pos)
        self.has_moved = False

    def get_valid_moves(self, board_map):
        row, col = self.current_pos[0], self.current_pos[1]
        moves = []

        move = self.add_move(board_map, (row + 1, col))
        if move is not None:
            moves.append(move)
        move = self.add_move(board_map, (row - 1, col))
        if move is not None:
            moves.append(move)
        move = self.add_move(board_map, (row + 1, col - 1))
        if move is not None:
            moves.append(move)
        move = self.add_move(board_map, (row - 1, col - 1))
        if move is not None:
            moves.append(move)
        move = self.add_move(board_map, (row + 1, col + 1))
        if move is not None:
            moves.append(move)
        move = self.add_move(board_map, (row - 1, col + 1))
        if move is not None:
            moves.append(move)
        move = self.add_move(board_map, (self.current_pos[0], self.current_pos[1] - 1))
        if move is not None:
            moves.append(move)
        move = self.add_move(board_map, (self.current_pos[0], self.current_pos[1] + 1))
        if move is not None:
            moves.append(move)

        move = self.add_move(board_map, (self.current_pos[0], self.current_pos[1] + 2))
        if self.castling_possible(move):
            move.is_castling = True
            moves.append(move)

        move = self.add_move(board_map, (self.current_pos[0], self.current_pos[1] - 3))
        if self.long_castling_possible(move):
            move.is_longcastling = True
            moves.append(move)
        return moves

    def castling_possible(self, move):
        # piece is white
        if not move:
            return False
        if self.own == 1:
            # piece is in king's original position
            if move.current_pos == (7, 4) and not self.has_moved:
                return True
        # piece is black
        if self.own == -1:
            if move.current_pos == (0, 4) and not self.has_moved:
                return True

        return False

    def long_castling_possible(self, move):
        # piece is white
        if not move:
            return False
        if self.own == 1:
            # piece is in king's original position
            if move.current_pos == (7, 4) and not self.has_moved:
                return True
        # piece is black
        if self.own == -1:
            if move.current_pos == (0, 4) and not self.has_moved:
                return True
        return True

    def initialize_king_move(self, board_map):
        move = Move()
        move.piece_type = king
        move.current_pos = self.current_pos
        return move

    def add_move(self, board_map, new_pos):
        row, col = new_pos[0], new_pos[1]
        if (0 <= row < board_map.shape[0]) and (0 <= col < board_map.shape[1]) \
                and board_map[row, col] != self.own:
            move = self.initialize_king_move(board_map)
            move.new_pos = (row, col)
            if board_map[row, col] == self.oppos:
                move.is_capture = True

            return move
        else:
            return None

    def __str__(self):
        return 'K'


class knight(piece):
    def __init__(self, color, current_pos):
        super().__init__(color, current_pos)
        self.has_moved = False

    def add_move(self, board_map, new_pos):
        row, col = new_pos[0], new_pos[1]
        if (0 <= row < board_map.shape[0]) and (0 <= col < board_map.shape[1]) \
                and board_map[row, col] != self.own:
            move = self.initialize_knight_move(board_map)
            move.new_pos = (row, col)
            if board_map[row, col] == self.oppos:
                move.is_capture = True

            return move
        else:
            return None

    def get_valid_moves(self, board_map):
        row, col = self.current_pos[0], self.current_pos[1]
        moves = []

        move1 = self.add_move(board_map, (row + 2, col - 1))
        if move1 is not None:
            moves.append(move1)
        move2 = self.add_move(board_map, (row + 2, col + 1))
        if move2 is not None:
            moves.append(move2)
        move3 = self.add_move(board_map, (row + 1, col - 2))
        if move3 is not None:
            moves.append(move3)
        move4 = self.add_move(board_map, (row + 1, col + 2))
        if move4 is not None:
            moves.append(move4)
        move5 = self.add_move(board_map, (row - 2, col + 1))
        if move5 is not None:
            moves.append(move5)
        move6 = self.add_move(board_map, (row - 2, col - 1))
        if move6 is not None:
            moves.append(move6)
        move7 = self.add_move(board_map, (row - 1, col - 2))
        if move7 is not None:
            moves.append(move7)
        move8 = self.add_move(board_map, (row - 1, col + 2))
        if move8 is not None:
            moves.append(move8)
        return moves

    def initialize_knight_move(self, board_map):
        move = Move()
        move.piece_type = knight
        move.current_pos = self.current_pos
        return move

    def __str__(self):
        return 'N'


class bishop(piece):
    def __init__(self, color, current_pos):
        super().__init__(color, current_pos)
        self.has_moved = False

    def get_valid_moves(self, board_map):
        row, col = self.current_pos[0], self.current_pos[1]
        moves = []
        i = 1
        while col + i < board_map.shape[1] and row + i < board_map.shape[0]:
            if board_map[row + i, col + i] != self.own:
                move = self.add_move(board_map, (row + i, col + i))
                if move is not None:
                    moves.append(move)
                if board_map[row + i, col + i] == self.oppos:
                    break
                i += 1
            else:
                break
        i = 1
        while col - i >= 0 and row + i < board_map.shape[0]:
            if board_map[row + i, col - i] != self.own:
                move = self.add_move(board_map, (row + i, col - i))
                if move is not None:
                    moves.append(move)
                if board_map[row + i, col - i] == self.oppos:
                    break
                i += 1
            else:
                break
        i = 1
        while row - i >= 0 and col - i >= 0:
            if board_map[row - i, col - i] != self.own:
                move = self.add_move(board_map, (row - i, col - i))
                if move is not None:
                    moves.append(move)
                if board_map[row - i, col - i] == self.oppos:
                    break
                i += 1

            else:
                break
        i = 1
        while row - i >= 0 and col + i < board_map.shape[1]:
            if board_map[row - i, col + i] != self.own:
                move = self.add_move(board_map, (row - i, col + i))
                if move is not None:
                    moves.append(move)
                if board_map[row - i, col + i] == self.oppos:
                    break
                i += 1
            else:
                break

        return moves

    def initialize_bishop_move(self, board_map):
        move = Move()
        move.piece_type = bishop
        move.current_pos = self.current_pos
        return move

    def add_move(self, board_map, new_pos):
        row, col = new_pos[0], new_pos[1]
        if (0 <= row < board_map.shape[0]) and (0 <= col < board_map.shape[1]) \
                and board_map[row, col] != self.own:
            move = self.initialize_bishop_move(board_map)
            move.new_pos = (row, col)
            if board_map[row, col] == self.oppos:
                move.is_capture = True

            return move
        else:
            return None

    def __str__(self):
        return 'B'
