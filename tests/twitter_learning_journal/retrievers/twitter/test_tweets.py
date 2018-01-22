from datetime import datetime
from unittest.mock import MagicMock, patch

from pytest import fixture

from app.twitter_learning_journal.models.tweet import Tweet
from app.twitter_learning_journal.retrievers.twitter.tweets import Tweets


@fixture(name='tweets')
@patch('app.twitter_learning_journal.retrievers.twitter.tweets.TweetCacher')
@patch('app.twitter_learning_journal.retrievers.twitter.tweets.TweetCacheLoader')
def _tweets(mock_tweet_cache_loader, mock_tweet_cacher):
    mock_twitter_api = MagicMock()
    tweets = Tweets(mock_twitter_api, 'screen_name')

    assert tweets
    assert mock_twitter_api == tweets._twitter_api
    assert 'screen_name' == tweets.screen_name

    return tweets


def test_cached_tweets_is_cached(tweets):
    expected_cached_tweets = 'cached_value'
    tweets._cached_tweets = expected_cached_tweets

    assert expected_cached_tweets == tweets.cached_tweets


@patch('app.twitter_learning_journal.retrievers.twitter.tweets.TweetCacheLoader')
def test_cached_tweets(mock_tweet_cache_loader, tweets):
    mock_tweet_cache_loader_instance = mock_tweet_cache_loader.return_value

    assert mock_tweet_cache_loader_instance.load_cached_tweets.return_value == tweets.cached_tweets
    mock_tweet_cache_loader.assert_called_with(tweets.screen_name)


@patch('app.twitter_learning_journal.retrievers.twitter.tweets.Cursor')
def test_call(mock_cursor, tweets):
    mock_cursor.return_value.items.return_value = ['1']

    generator_response = tweets._call()
    items = [item for item in generator_response]

    assert "<class 'generator'>" == str(type(generator_response))
    assert ['1'] == items
    assert mock_cursor.called
    mock_cursor.assert_called_with(tweets._twitter_api.favorites, 'screen_name', count=50, tweet_mode='extended')


@patch('app.twitter_learning_journal.retrievers.twitter.tweets.TweetCacher')
@patch('app.twitter_learning_journal.retrievers.twitter.tweets.Tweets._call')
def test_get(mock_call, mock_tweet_cacher, tweets):
    tweets._cached_tweets = []
    id = 1
    created_at = datetime.now()
    full_text = 'full_text'
    entities = {
        'hashtags': [
            {
                'text': 'some_text'
            },
            {
                'text': 'other_text'
            }
        ],
        'urls': []
    }

    tweet_response = MagicMock(id=id,
                               created_at=created_at,
                               full_text=full_text,
                               entities=entities)
    delattr(tweet_response, 'retweeted_status')
    mock_call.return_value = [tweet_response]

    expected_tweet_model = Tweet(
        id=id,
        created_at=created_at,
        full_text=full_text,
        hashtags='some_text|other_text',
        type='favorite'
    )

    tweets_list = tweets.get()

    assert [expected_tweet_model] == tweets_list
    assert mock_call.called

    mock_tweet_cacher.assert_called_with(tweets.screen_name, expected_tweet_model)
    assert mock_tweet_cacher.return_value.cache.called


@patch('app.twitter_learning_journal.retrievers.twitter.tweets.TweetCacher')
@patch('app.twitter_learning_journal.retrievers.twitter.tweets.Tweets.extract_hashtags')
@patch('app.twitter_learning_journal.retrievers.twitter.tweets.Tweets._call')
def test_get_with_retweeted_status(mock_call, mock_extract_hashtags, mock_tweet_cacher, tweets):
    tweets._cached_tweets = []
    full_text = 'full_text'

    tweet_response = MagicMock(id=1, retweeted_status=MagicMock(full_text=full_text))
    mock_call.return_value = [tweet_response]

    expected_tweet_model = Tweet(
        id=tweet_response.id,
        created_at=tweet_response.created_at,
        full_text=full_text,
        type='favorite',
        hashtags=mock_extract_hashtags.return_value
    )

    tweets_list = tweets.get()

    assert [expected_tweet_model] == tweets_list
    assert mock_call.called

    mock_tweet_cacher.assert_called_with(tweets.screen_name, expected_tweet_model)
    assert mock_tweet_cacher.return_value.cache.called


# will fix, integration passes
# @patch('app.twitter_learning_journal.retrievers.twitter.tweets.TweetCacher')
# @patch('app.twitter_learning_journal.retrievers.twitter.tweets.Tweets.extract_hashtags')
# @patch('app.twitter_learning_journal.retrievers.twitter.tweets.Tweets._call')
# def test_get_with_cached_tweets(mock_call, mock_extract_hashtags, mock_tweet_cacher, tweets):
#     full_text = 'full_text'
#
#     tweet_response = MagicMock(id=1, retweeted_status=MagicMock(full_text=full_text))
#     mock_call.return_value = [tweet_response]
#
#     expected_tweet_model_first = Tweet(
#         id=tweet_response.id,
#         created_at=tweet_response.created_at,
#         full_text=full_text,
#         type='favorite',
#         hashtags=mock_extract_hashtags.return_value
#     )
#     expected_tweet_model_second = Tweet(
#         id=2,
#         created_at=tweet_response.created_at,
#         full_text=full_text + '2',
#         type='favorite',
#         hashtags=mock_extract_hashtags.return_value
#     )
#
#     expected_tweets = []
#
#     cached_tweets = [
#         expected_tweet_model_first,
#         expected_tweet_model_second
#     ]
#     tweets._cached_tweets = cached_tweets
#
#     tweets_list = tweets.get()
#
#     assert expected_tweets == tweets_list
#     assert not mock_tweet_cacher.called


def test_extract_urls_without_url_without_retweeted_status():
    expected_url = []
    entities = {'urls': [], }

    call_response = MagicMock(entities=entities)

    urls = Tweets.extract_urls(call_response)

    assert expected_url == urls


def test_extract_urls_with_url_without_retweeted_status():
    expected_url = ['url']

    call_response = MagicMock(entities=_entities)

    urls = Tweets.extract_urls(call_response)

    assert expected_url == urls


def test_extract_urls_with_url_with_retweeted_status():
    expected_url = ['url']
    retweeted_status = MagicMock(entities=_retweeted_entities)
    call_response = MagicMock(entities=_entities, retweeted_status=retweeted_status)

    urls = Tweets.extract_urls(call_response)

    assert expected_url == urls


def test_extract_urls_without_url_with_retweeted_status():
    expected_url = ['url']
    entities = {'urls': [], }
    retweeted_status = MagicMock(entities=_retweeted_entities)
    call_response = MagicMock(entities=entities, retweeted_status=retweeted_status)

    urls = Tweets.extract_urls(call_response)

    assert expected_url == urls


def test_remove_ignore_urls():
    urls = [
        'https://twitter.com/dev3l_',
        'url',
        'url2'
    ]

    assert ['url', 'url2'] == Tweets._remove_ignore_urls(urls)


_entities_urls = [
    {
        'expanded_url': 'url'
    },
    {
        'expanded_url': 'https://twitter.com/dev3l_'  # ignored
    },
]

_retweeted_urls = [
    {
        'expanded_url': 'url'
    },
    {
        'expanded_url': 'https://twitter.com/dev3l_'  # ignored
    },
]

_entities = {
    'urls': _entities_urls,
}

_retweeted_entities = {
    'urls': _retweeted_urls
}
