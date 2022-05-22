import initializations as init
import Piece
import numpy as np



class Player:
    '''Contains collection of pieces of both sides'''
    def __init__(self, color):
        self.color = color
        self.pieces = init.initialize_pieces(color)

def update_turn(turn):
    if turn == 0: return 1
    elif turn==1: return 0

    
def get_possible_moves(cur_pieces, board_map):
    return [piece.get_valid_moves() for piece in cur_pieces]

def select(move_notation, valid_moves):
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
    m = re.match(pattern=pattern, string=move)
    m_dict = m.groupdict()
    piece_type = Pawn

    # region determining piece type
    if m_dict['piece'] != '':
        if m_dict['piece'] == 'R':
            piece_type = Rook
        elif m_dict['piece'] == 'Q': 
            piece_type = Queen
        elif m_dict['piece'] == 'N':
            piece_type = Knight
        elif m_dict['piece'] == 'B':
            piece_type = Bishop
        else:
            piece_type = King
    # endregion
    return valid_moves[0]

def start_game():
    turn = 0
    timer1 = 300
    timer2 = 300
    board_map= np.zeros((8, 8))
    current_game = ""
    player1 = Player("white")
    player2 = Player("black")
    board_map[-2] = 1
    board_map[1] = -1
    
    
    while True:
        if turn == 0: cur_pieces = player1.pieces
        elif turn == 1: cur_pieces  = player2.pieces
        
        move_notation = str(input())
        valid_moves = get_possible_moves(cur_pieces, board_map)
        move = select(move_notation, valid_moves)
        turn = update_turn(turn)



    turn = update_turn(turn)

if __name__ == "__main__": 
	start_game()
	
