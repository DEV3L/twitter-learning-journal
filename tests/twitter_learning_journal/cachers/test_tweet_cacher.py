from unittest.mock import patch

from pytest import fixture

from app.twitter_learning_journal.cachers.tweet_cacher import TweetCacher
from app.twitter_learning_journal.models.tweet import Tweet

expected_cache_path = './data/pickle/tweets/screen name'
expected_screen_name = 'screen name'


@fixture(name='tweet_cacher_tuple')
@patch('app.twitter_learning_journal.cachers.tweet_cacher.Cacher._init_cache_dir')
def _tweet_cacher_tuple(mock_init_cache_dir):
    tweet = Tweet(id=1)
    tweet_cacher = TweetCacher(expected_screen_name, tweet)
    assert mock_init_cache_dir.called

    return tweet_cacher, tweet


def test_tweet_cacher_init(tweet_cacher_tuple):
    expected_tweet = tweet_cacher_tuple[1]
    expected_file_path = f'{expected_cache_path}/{expected_tweet.id}'
    tweet_cacher = tweet_cacher_tuple[0]

    assert expected_cache_path == tweet_cacher.cache_path
    assert expected_file_path == tweet_cacher.file_path
    assert expected_tweet == tweet_cacher.tweet
