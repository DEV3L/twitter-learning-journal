from unittest.mock import patch

from pytest import fixture

from app.twitter_learning_journal.database.sqlalchemy_database import Database


@fixture(name='database')
@patch('app.twitter_learning_journal.database.sqlalchemy_database.sessionmaker')
@patch('app.twitter_learning_journal.database.sqlalchemy_database.create_engine')
def _database(mock_create_engine, mock_sessionmaker):
    database = Database()

    assert database
    assert mock_create_engine.return_value == database._engine
    assert mock_sessionmaker.return_value.return_value == database._session

    mock_create_engine.assert_called_with('sqlite:///data/twitter-learning-journal', echo=True)
    mock_sessionmaker.assert_called_with(bind=mock_create_engine.return_value)

    return database


def test_add(database):
    mock_session = database._session

    entity = database.add('entity')

    assert mock_session.add.return_value == entity
    mock_session.add.assert_called_with('entity')


def test_query(database):
    mock_session = database._session

    entity = database.query('entity')

    assert mock_session.query.return_value == entity
    mock_session.query.assert_called_with('entity')


def test_commit(database):
    mock_session = database._session

    assert not database.commit()
    assert mock_session.commit.called
