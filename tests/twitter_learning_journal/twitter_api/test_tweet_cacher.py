from unittest.mock import MagicMock

from app.twitter_learning_journal.twitter_api.tweet_cacher import TweetCacher


def test_tweet_cacher_init():
    expected_cache_path = './data/pickle/tweets/'
    mock_tweet = MagicMock()

    tweet_cacher = TweetCacher(mock_tweet)

    assert expected_cache_path == tweet_cacher.cache_path
    assert mock_tweet == tweet_cacher.tweet


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
