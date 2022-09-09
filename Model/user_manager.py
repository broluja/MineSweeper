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

    @staticmethod
    def get_model(player):
        return Player(player_name=player[0], games_played=player[1], games_won=player[2])

    def commit(self):
        self.conn.commit()
        self.conn.close()

    def connect(self):
        self.conn = sqlite3.connect('minesweeper.db')
        self.cursor = self.conn.cursor()

    def get_or_create_player(self, name):
        if player := self.conn.execute('SELECT * FROM players where player=?;', (name,)).fetchone():
            player = self.get_model(player)
            print(player)
            return player.player_name
        player = name
        games_played, games_won = 0, 0
        self.conn.execute('INSERT INTO players VALUES(?, ?, ?);', (player, games_played, games_won))
        return player

    def record_win(self, name):
        player = self.conn.execute('SELECT * FROM players WHERE player=?', (name, )).fetchone()
        player = self.get_model(player)
        games_played, games_won = player.games_played, player.games_won
        games_played += 1
        games_won += 1
        sql_command = 'UPDATE players SET games_played=?, games_won=? WHERE player=?;'
        self.conn.execute(sql_command, (games_played, games_won, name))
        return player

    def record_loss(self, name):
        player = self.conn.execute('SELECT * FROM players WHERE player=?', (name, )).fetchone()
        player = self.get_model(player)
        game_played = player.games_played
        game_played += 1
        sql_command = 'UPDATE players SET games_played=? WHERE player=?;'
        self.conn.execute(sql_command, (game_played, name))
        return player.player_name, game_played


user_manager = UserManager()
