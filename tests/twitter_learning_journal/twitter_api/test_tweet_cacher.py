from unittest.mock import patch

from pytest import fixture

from app.twitter_learning_journal.models.tweet import Tweet
from app.twitter_learning_journal.twitter_api.tweet_cacher import TweetCacher

expected_cache_path = './data/pickle/tweets/screen name'
expected_screen_name = 'screen name'


@fixture(name='tweet_cacher_tuple')
@patch('app.twitter_learning_journal.twitter_api.tweet_cacher.Cacher._init_cache_dir')
def _tweet_cacher_tuple(mock_init_cache_dir):
    tweet = Tweet(id=1)
    tweet_cacher = TweetCacher(expected_screen_name, tweet)
    assert mock_init_cache_dir.called

    return tweet_cacher, tweet


def test_tweet_cacher_init(tweet_cacher_tuple):
    expected_tweet = tweet_cacher_tuple[1]
    expected_file_path = f'{expected_cache_path}{expected_tweet.id}'
    tweet_cacher = tweet_cacher_tuple[0]

    assert expected_cache_path == tweet_cacher.cache_path
    assert expected_file_path == tweet_cacher.file_path
    assert expected_tweet == tweet_cacher.tweet


@patch('app.twitter_learning_journal.twitter_api.tweet_cacher.path')
def test_is_cached(mock_path, tweet_cacher_tuple):
    expected_is_cached = True
    mock_path.isfile.return_value = expected_is_cached
    expected_file_path = f'{expected_cache_path}1'
    tweet_cacher = tweet_cacher_tuple[0]

    is_cached = tweet_cacher.is_cached()

    assert expected_is_cached == is_cached
    mock_path.isfile.assert_called_with(expected_file_path)


@patch('app.twitter_learning_journal.twitter_api.tweet_cacher.path')
def test_is_not_cached(mock_path, tweet_cacher_tuple):
    expected_is_cached = False
    mock_path.isfile.return_value = expected_is_cached
    expected_file_path = f'{expected_cache_path}1'

    tweet_cacher = tweet_cacher_tuple[0]
    is_cached = tweet_cacher.is_cached()

    assert expected_is_cached == is_cached
    mock_path.isfile.assert_called_with(expected_file_path)


@patch('app.twitter_learning_journal.twitter_api.tweet_cacher.write_pickle_data')
def test_cache(mock_write_pickle_data, tweet_cacher_tuple):
    tweet = tweet_cacher_tuple[1]
    tweet_cacher = tweet_cacher_tuple[0]

    tweet_cacher.cache()

    mock_write_pickle_data.assert_called_with(tweet, tweet_cacher.file_path)


@patch('app.twitter_learning_journal.twitter_api.tweet_cacher.load_pickle_data')
def test_get(mock_load_pickle_data, tweet_cacher_tuple):
    expected_tweet = tweet_cacher_tuple[1]
    mock_load_pickle_data.return_value = expected_tweet

    tweet_cacher = tweet_cacher_tuple[0]

    tweet = tweet_cacher.get()

    assert expected_tweet == tweet
    mock_load_pickle_data.assert_called_with(tweet_cacher.file_path)
