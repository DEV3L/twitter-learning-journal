from unittest.mock import MagicMock, patch, ANY

from pytest import fixture

from app.twitter_learning_journal.dao.favorite_dao import FavoriteDao
from app.twitter_learning_journal.models.favorite import Favorite


@fixture(name='favorite_dao')
def _favorite_dao():
    mock_database = MagicMock()
    favorite_dao = FavoriteDao(mock_database)

    assert favorite_dao
    assert mock_database == favorite_dao._database

    return favorite_dao


@fixture(name='favorite')
def _favorite():
    return Favorite(id=1)


@patch('app.twitter_learning_journal.dao.favorite_dao.Favorite')
@patch('app.twitter_learning_journal.dao.favorite_dao.exists')
def test_exists(mock_exists, mock_favorite, favorite_dao):
    mock_database = favorite_dao._database
    mock_database.query.return_value.scalar.return_value = False

    assert not favorite_dao.exists(0)
    mock_database.query.assert_called_with(mock_exists.return_value.where.return_value)
    mock_exists.return_value.where.assert_called_with(ANY)
    mock_favorite.id.__eq__.assert_called_with(0)


@patch('app.twitter_learning_journal.dao.favorite_dao.Favorite')
def test_by_id(mock_favorite, favorite_dao, favorite):
    mock_database = favorite_dao._database
    mock_database.query.return_value.filter.return_value.first.return_value = favorite

    assert favorite_dao.by_id(1) == favorite
    mock_favorite.id.__eq__.assert_called_with(1)


def test_by_id_not_found(favorite_dao):
    mock_database = favorite_dao._database
    mock_database.query.return_value.filter.return_value.first.return_value = None

    assert favorite_dao.by_id(0) == None
    mock_database.query.assert_called_with(Favorite)


def test_query_all(favorite_dao, favorite):
    mock_database = favorite_dao._database
    mock_database.query.return_value.all.return_value = [favorite]

    assert [favorite] == favorite_dao.query_all()
    mock_database.query.assert_called_with(Favorite)


def test_add(favorite_dao, favorite):
    mock_database = favorite_dao._database

    favorite_dao.add(favorite)

    mock_database.add.assert_called_with(favorite)


def test_add_all(favorite_dao, favorite):
    mock_database = favorite_dao._database

    favorite_dao.add_all([favorite])

    mock_database.add_all.assert_called_with([favorite])
