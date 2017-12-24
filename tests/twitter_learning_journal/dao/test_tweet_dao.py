from unittest.mock import MagicMock, patch, ANY

from pytest import fixture

from app.twitter_learning_journal.dao.tweet_dao import TweetDao
from app.twitter_learning_journal.models.tweet import Tweet


@fixture(name='tweet_dao')
def _tweet_dao():
    mock_database = MagicMock()
    tweet_dao = TweetDao(mock_database)

    assert tweet_dao
    assert mock_database == tweet_dao._database

    return tweet_dao


@fixture(name='tweet')
def _tweet():
    return Tweet(id=1)


@patch('app.twitter_learning_journal.dao.tweet_dao.Tweet')
@patch('app.twitter_learning_journal.dao.tweet_dao.exists')
def test_exists(mock_exists, mock_tweet, tweet_dao):
    mock_database = tweet_dao._database
    mock_database.query.return_value.scalar.return_value = False

    assert not tweet_dao.exists(0)
    mock_database.query.assert_called_with(mock_exists.return_value.where.return_value)
    mock_exists.return_value.where.assert_called_with(ANY)
    mock_tweet.id.__eq__.assert_called_with(0)


@patch('app.twitter_learning_journal.dao.tweet_dao.Tweet')
def test_by_id(mock_tweet, tweet_dao, tweet):
    mock_database = tweet_dao._database
    mock_database.query.return_value.filter.return_value.first.return_value = tweet

    assert tweet_dao.by_id(1) == tweet
    mock_tweet.id.__eq__.assert_called_with(1)


def test_by_id_not_found(tweet_dao):
    mock_database = tweet_dao._database
    mock_database.query.return_value.filter.return_value.first.return_value = None

    assert tweet_dao.by_id(0) == None
    mock_database.query.assert_called_with(Tweet)


def test_query_all(tweet_dao, tweet):
    mock_database = tweet_dao._database
    mock_database.query.return_value.all.return_value = [tweet]

    assert [tweet] == tweet_dao.query_all()
    mock_database.query.assert_called_with(Tweet)


def test_add(tweet_dao, tweet):
    mock_database = tweet_dao._database

    tweet_dao.add(tweet)

    mock_database.add.assert_called_with(tweet)


def test_add_all(tweet_dao, tweet):
    mock_database = tweet_dao._database

    tweet_dao.add_all([tweet])

    mock_database.add_all.assert_called_with([tweet])


def test_commit(tweet_dao):
    mock_database = tweet_dao._database

    tweet_dao.commit()

    mock_database.commit.assert_called_with()
