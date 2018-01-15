from unittest.mock import patch, MagicMock

from pytest import fixture

from app.twitter_learning_journal.database.sqlalchemy_database import Database, build_tables


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


@patch('app.twitter_learning_journal.database.sqlalchemy_database.sessionmaker')
@patch('app.twitter_learning_journal.database.sqlalchemy_database.create_engine')
def test_database_database_url(mock_create_engine, mock_sessionmaker):
    Database(database_url='test_url')

    mock_create_engine.assert_called_with('sqlite:///test_url', echo=True)
    mock_sessionmaker.assert_called_with(bind=mock_create_engine.return_value)


def test_add(database):
    mock_session = database._session

    database.add('entity')

    mock_session.add.assert_called_with('entity')


def test_add_all(database):
    mock_session = database._session

    database.add_all(['entity'])

    mock_session.add_all.assert_called_with(['entity'])


def test_query(database):
    mock_session = database._session

    entity = database.query('entity')

    assert mock_session.query.return_value == entity
    mock_session.query.assert_called_with('entity')


def test_commit(database):
    mock_session = database._session

    assert not database.commit()
    assert mock_session.commit.called


@patch('app.twitter_learning_journal.database.sqlalchemy_database.Base')
def test_build_tables(mock_base):
    mock_database = MagicMock()

    build_tables(mock_database)

    mock_base.metadata.create_all.assert_called_with(mock_database._engine)
