from unittest.mock import MagicMock, patch

from app.twitter_learning_journal.retrievers.twitter_retriever import TwitterRetriever


@patch('app.twitter_learning_journal.retrievers.twitter_retriever.get_api')
def test_init_twitter_retriever(mock_get_api):
    mock_tweet_dao = MagicMock()
    screen_name = 'screen_name'

    twitter_retriever = TwitterRetriever(mock_tweet_dao, screen_name)

    assert screen_name == twitter_retriever.screen_name
    assert mock_tweet_dao == twitter_retriever.tweet_dao
    assert twitter_retriever.api == mock_get_api.return_value


@patch('app.twitter_learning_journal.retrievers.twitter_retriever.Tweets')
def test_fetch_protected(mock_tweets):
    mock_api = MagicMock()

    twitter_retriever = TwitterRetriever(None, 'screen name')
    twitter_retriever.api = mock_api

    tweets = twitter_retriever._fetch('tweet_type')

    assert mock_tweets.return_value.get.return_value == tweets
    mock_tweets.assert_called_with(mock_api, 'screen name', tweet_type='tweet_type')


def test_save_tweets():
    mock_tweet_dao = MagicMock()
    mock_tweet_dao.exists.return_value = False

    twitter_retriever = TwitterRetriever(mock_tweet_dao, 'screen name')

    mock_tweet = MagicMock(id=1)
    tweets = [mock_tweet]

    twitter_retriever._save_tweets(tweets)

    mock_tweet_dao.exists.assert_called_with(1)
    mock_tweet_dao.add.assert_called_with(mock_tweet)
    assert mock_tweet_dao.commit.called


def test_fetch():
    expected_tweets = ['test', 'test']
    mock_fetch_protected = MagicMock()
    mock_fetch_protected.return_value = ['test']

    mock_save_tweets = MagicMock()

    twitter_retriever = TwitterRetriever(None, 'screen name')
    twitter_retriever._fetch = mock_fetch_protected
    twitter_retriever._save_tweets = mock_save_tweets

    tweets = twitter_retriever.fetch()

    assert 'favorite' == mock_fetch_protected.call_args[0][0]
    assert 2 == mock_fetch_protected.call_count
    mock_save_tweets.assert_called_with(expected_tweets)

    assert expected_tweets == tweets
