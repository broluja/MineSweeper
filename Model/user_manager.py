import sqlite3
import os

from Model.player import Player

home_location = os.environ['MINESWEEPER']


class UserManager(object):
    """Class for interaction with database table 'players'."""
    INSTRUCTION = 'CREATE TABLE IF NOT EXISTS players(player TEXT UNIQUE, games_played INT, games_won INT)'

    def __init__(self):
        self.conn = sqlite3.connect(f'{home_location}/minesweeper.db')
        self.cursor = self.conn.cursor()
        self.cursor.execute(self.INSTRUCTION)
        self.commit()

    def __enter__(self):
        self.connect()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type is None:
            self.commit()
            print('Data stored.')
        else:
            self.commit()
            print(f'File closed but an exception appeared: {str(exc_type)}')
            return False

    def __str__(self):
        return f'User Manager for {self.conn}'

    def commit(self):
        self.conn.commit()
        self.conn.close()

    def connect(self):
        self.conn = sqlite3.connect('minesweeper.db')
        self.cursor = self.conn.cursor()

    def get_or_create_player(self, name):
        if player := self.conn.execute('SELECT * FROM players where player=?;', (name,)).fetchall():
            player = Player(player_name=player[0][0], games_played=player[0][1], games_won=player[0][2])
            return player.player_name
        player = name
        games_played, games_won = 0, 0
        self.conn.execute('INSERT INTO players VALUES(?, ?, ?);', (player, games_played, games_won))
        return player

    def record_win(self):
        pass

    def record_loss(self):
        pass

    # def check_email_usage(self, email: str):
    #     sql_command = 'SELECT * FROM players WHERE email=?;'
    #     self.cursor.execute(sql_command, (email,))
    #     return self.cursor.fetchone()

    # def register_user(self, user_id: str, email: str, password: str):
    #     sql_command = 'INSERT INTO users VALUES(?, ?, ?);'
    #     self.cursor.execute(sql_command, (user_id, email, password))


user_manager = UserManager()
