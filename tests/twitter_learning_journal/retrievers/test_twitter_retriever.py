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
