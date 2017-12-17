from unittest.mock import patch

from app.twitter_learning_journal.database.sqlite_database import Database


@patch('app.twitter_learning_journal.database.sqlite_database.sqlite3')
def test_sqlite_database(mock_sqlite3):
    database = Database()

    assert database
    assert database._db

    mock_sqlite3.connect.assert_called_with('data/twitter-learning-journal')
