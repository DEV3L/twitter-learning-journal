from unittest.mock import patch, MagicMock

from pytest import fixture

from app.twitter_learning_journal.twitter_api.tweet_cache_loader import TweetCacheLoader

expected_cache_path = './data/pickle/tweets/screen name'
expected_screen_name = 'screen name'

@fixture(name='tweet_cache_loader')
@patch('app.twitter_learning_journal.twitter_api.tweet_cacher.Cacher._init_cache_dir')
def _tweet_cache_loader(mock_init_cache_dir):
    tweet_cache_loader = TweetCacheLoader(expected_screen_name)
    assert mock_init_cache_dir.called
    return tweet_cache_loader


def test_tweet_cache_loader_init(tweet_cache_loader):
    assert expected_screen_name == tweet_cache_loader.screen_name
    assert expected_cache_path == tweet_cache_loader.cache_path


@patch('app.twitter_learning_journal.twitter_api.tweet_cache_loader.load_pickle_data')
def test_load_cached_tweet(mock_load_pickle_data, tweet_cache_loader):
    expected_file_path = 'test'
    expected_tweet = mock_load_pickle_data.return_value

    tweet = tweet_cache_loader._load_cached_tweet('test')

    assert expected_tweet == tweet
    mock_load_pickle_data.assert_called_with(expected_file_path)


@patch('app.twitter_learning_journal.twitter_api.tweet_cache_loader.Path')
def test_load_cached_tweets(mock_path, tweet_cache_loader):
    _object = 'test'
    expected_cached_tweets = [_object]

    mock_load_cached_tweet = MagicMock()
    mock_load_cached_tweet.return_value = _object
    tweet_cache_loader._load_cached_tweet = mock_load_cached_tweet

    mock_cache_dir = MagicMock()
    mock_cache_dir.iterdir.return_value = [_object]

    mock_path.return_value = mock_cache_dir

    cached_tweets = tweet_cache_loader.load_cached_tweets()

    assert expected_cached_tweets == cached_tweets
    mock_load_cached_tweet.assert_called_with(_object)
    mock_path.assert_called_with(tweet_cache_loader.cache_path)
