from unittest.mock import patch

from app.twitter_learning_journal.models.tweet import Tweet
from app.twitter_learning_journal.twitter_api.tweet_cacher import TweetCacher

expected_cache_path = './data/pickle/tweets/screen name'
expected_screen_name = 'screen name'


@patch('app.twitter_learning_journal.twitter_api.tweet_cacher.TweetCacher._init_cache_dir')
def test_tweet_cacher_init(mock_init_cache_dir):
    expected_tweet = Tweet()

    tweet_cacher = TweetCacher(expected_screen_name, expected_tweet)

    assert expected_cache_path == tweet_cacher.cache_path
    assert expected_tweet == tweet_cacher.tweet
    assert mock_init_cache_dir.called


@patch('app.twitter_learning_journal.twitter_api.tweet_cacher.makedirs')
@patch('app.twitter_learning_journal.twitter_api.tweet_cacher.path')
def test_init_cache_dir_exists(mock_path, mock_makedirs):
    mock_path.isdir.return_value = True

    tweet_catch = TweetCacher(expected_screen_name, Tweet())

    mock_path.isdir.assert_called_with(tweet_catch.cache_path)
    assert not mock_makedirs.called


@patch('app.twitter_learning_journal.twitter_api.tweet_cacher.makedirs')
@patch('app.twitter_learning_journal.twitter_api.tweet_cacher.path')
def test_init_cache_dir_not_exists(mock_path, mock_makedirs):
    mock_path.isdir.return_value = False

    tweet_catch = TweetCacher(expected_screen_name, Tweet())

    mock_path.isdir.assert_called_with(tweet_catch.cache_path)
    mock_makedirs.assert_called_with(tweet_catch.cache_path)

"""

def _get_url(url):
    url_sha = f'{pickle_dir}{_sha_url(url)}'

    try:
        response = pickle.load(open(url_sha, 'rb'))
    except:
        response = requests.get(url)
        pickle.dump(response, open(url_sha, 'wb'))
        time.sleep(5)

    return response
"""
