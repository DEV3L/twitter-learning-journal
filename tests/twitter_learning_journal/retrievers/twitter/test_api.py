import os
from unittest.mock import patch

from app.twitter_learning_journal.retrievers.twitter.api import get_api, get_auth_handler


@patch('app.twitter_learning_journal.retrievers.twitter.api.get_auth_handler')
@patch('app.twitter_learning_journal.retrievers.twitter.api.tweepy')
def test_get_api(mock_tweepy, mock_get_auth_handler):
    api = get_api()

    mock_tweepy.API.assert_called_with(mock_get_auth_handler.return_value,
                                       wait_on_rate_limit=True, wait_on_rate_limit_notify=True)

    assert mock_tweepy.API.return_value == api


@patch('app.twitter_learning_journal.retrievers.twitter.api.tweepy')
def test_get_auth_handler(mock_tweepy):
    os.environ['TWITTER_CONSUMER_KEY'] = 'twitter_consumer_key'
    os.environ['TWITTER_CONSUMER_SECRET'] = 'twitter_consumer_secret'
    os.environ['TWITTER_ACCESS_TOKEN'] = 'twitter_access_token'
    os.environ['TWITTER_TOKEN_SECRET'] = 'twitter_token_secret'

    auth_handler = get_auth_handler()

    mock_tweepy.OAuthHandler.assert_called_with('twitter_consumer_key', 'twitter_consumer_secret')
    mock_tweepy.OAuthHandler.return_value.set_access_token.assert_called_with('twitter_access_token',
                                                                              'twitter_token_secret')

    assert mock_tweepy.OAuthHandler.return_value == auth_handler
