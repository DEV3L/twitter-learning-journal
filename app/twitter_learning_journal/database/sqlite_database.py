import sqlite3


class Database():
    def __init__(self):
        self._db = sqlite3.connect('data/twitter-learning-journal')
