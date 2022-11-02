import sqlite3
from sqlite3 import Connection


def create_game_table(conn: Connection):
    with conn:
        conn.execute('''CREATE TABLE IF NOT EXISTS game (
                              id INTEGER PRIMARY KEY UNIQUE NOT NULL
                            , name text default ''
                            )
            ''')
        check_table_exists(conn, 'game')


def drop_table(conn: Connection, table_name: str):
    with conn:
        drop_table_statement = '''DROP TABLE IF EXISTS {}'''.format(table_name)
        cursor = conn.cursor()
        cursor.execute(drop_table_statement)
        print(cursor.description)


def create_player_table(conn: Connection):
    with conn:
        conn.execute('''CREATE TABLE IF NOT EXISTS player (
                              id INTEGER PRIMARY KEY UNIQUE NOT NULL
                            , game_id INTEGER NOT NULL
                            , name text default 'player'
           
                            , time_remaining INTEGER
                            , color INTEGER CHECK (color = 0 or color = 1)
                            , FOREIGN KEY(game_id) references game(id) on delete cascade
                            )
            ''')
        check_table_exists(conn, 'player')


def create_pieces_table(conn: Connection):
    with conn:
        conn.execute('''CREATE TABLE IF NOT EXISTS piece (
                              id INTEGER PRIMARY KEY UNIQUE NOT NULL
                            , game_id INTEGER NOT NULL
                            , player_id INTEGER NOT NULL
                            , type INTEGER
                            , cur_row INTEGER
                            , cur_col integer
                            , has_moved INTEGER DEFAULT 0
                            , FOREIGN KEY(game_id) references game(id) on delete cascade
                            , FOREIGN KEY(player_id) references player(id) on delete cascade
                            )
            ''')
        check_table_exists(conn, 'piece')


def create_moves_table(conn: Connection):
    with conn:
        conn.execute('''CREATE TABLE IF NOT EXISTS move (
                              id INTEGER PRIMARY KEY UNIQUE NOT NULL
                            , game_id INTEGER NOT NULL
                            , player_id INTEGER NOT NULL
                            , piece_id INTEGER NOT NULL
                            , type INTEGER
                            , new_row INTEGER
                            , new_pos integer
                            , is_capture INTEGER
                            , FOREIGN KEY(game_id) references game(id) on delete cascade
                            , FOREIGN KEY(player_id) references player(id) on delete cascade
                            , FOREIGN KEY(piece_id) references piece(id) on delete cascade
                            )
            ''')
        check_table_exists(conn, 'player')


def check_table_exists(conn: Connection, table_name: str) -> bool:
    check_table_query = '''SELECT name FROM sqlite_master WHERE type='table' AND name=?;'''
    with conn:
        cursor = conn.cursor()
        cursor.execute(check_table_query, (table_name,))
        print(cursor.rowcount)
        if cursor.rowcount > 0:
            print('table {} exists in database'.format(table_name))
            return True
        print('table {} does not exist in database'.format(table_name))
    return False


def main():
    conn = sqlite3.connect('game_db.sqlite')
    drop_table(conn, 'move')
    drop_table(conn, 'piece')
    drop_table(conn, 'player')
    drop_table(conn, 'game')
    create_game_table(conn)
    create_player_table(conn)
    create_pieces_table(conn)
    create_moves_table(conn)


if __name__ == "__main__":
    main()
