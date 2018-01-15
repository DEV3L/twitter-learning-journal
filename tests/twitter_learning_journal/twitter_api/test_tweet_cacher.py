from unittest.mock import patch

from app.twitter_learning_journal.models.tweet import Tweet
from app.twitter_learning_journal.twitter_api.tweet_cacher import TweetCacher

expected_cache_path = './data/pickle/tweets/screen name'
expected_screen_name = 'screen name'


@patch('app.twitter_learning_journal.twitter_api.tweet_cacher.TweetCacher._init_cache_dir')
def test_tweet_cacher_init(mock_init_cache_dir):
    expected_tweet = Tweet(id=1)
    expected_file_path = f'{expected_cache_path}{expected_tweet.id}'
    tweet_cacher = TweetCacher(expected_screen_name, expected_tweet)

    assert expected_cache_path == tweet_cacher.cache_path
    assert expected_file_path == tweet_cacher.file_path
    assert expected_tweet == tweet_cacher.tweet
    assert mock_init_cache_dir.called


@patch('app.twitter_learning_journal.twitter_api.tweet_cacher.makedirs')
@patch('app.twitter_learning_journal.twitter_api.tweet_cacher.path')
def test_init_cache_dir_exists(mock_path, mock_makedirs):
    mock_path.isdir.return_value = True

    tweet_cache = TweetCacher(expected_screen_name, Tweet())

    mock_path.isdir.assert_called_with(tweet_cache.cache_path)
    assert not mock_makedirs.called


@patch('app.twitter_learning_journal.twitter_api.tweet_cacher.makedirs')
@patch('app.twitter_learning_journal.twitter_api.tweet_cacher.path')
def test_init_cache_dir_not_exists(mock_path, mock_makedirs):
    mock_path.isdir.return_value = False

    tweet_cache = TweetCacher(expected_screen_name, Tweet())

    mock_path.isdir.assert_called_with(tweet_cache.cache_path)
    mock_makedirs.assert_called_with(tweet_cache.cache_path)


@patch('app.twitter_learning_journal.twitter_api.tweet_cacher.path')
def test_is_cached(mock_path):
    expected_is_cached = True
    mock_path.isfile.return_value = expected_is_cached
    expected_file_path = f'{expected_cache_path}1'

    tweet = Tweet(id=1)
    tweet_cache = TweetCacher(expected_screen_name, tweet)

    is_cached = tweet_cache.is_cached()

    assert expected_is_cached == is_cached
    mock_path.isfile.assert_called_with(expected_file_path)


@patch('app.twitter_learning_journal.twitter_api.tweet_cacher.path')
def test_is_not_cached(mock_path):
    expected_is_cached = False
    mock_path.isfile.return_value = expected_is_cached
    expected_file_path = f'{expected_cache_path}1'

    tweet = Tweet(id=1)
    tweet_cache = TweetCacher(expected_screen_name, tweet)

    is_cached = tweet_cache.is_cached()

    assert expected_is_cached == is_cached
    mock_path.isfile.assert_called_with(expected_file_path)
