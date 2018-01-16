from unittest.mock import MagicMock

from app.twitter_learning_journal.retrievers.twitter_retriever import TwitterRetriever


def test_init_twitter_retriever():
    mock_api = MagicMock()
    screen_name = 'screen_name'

    twitter_retriever = TwitterRetriever(mock_api, screen_name)

    assert mock_api == twitter_retriever.api
    assert screen_name == twitter_retriever.screen_name
    assert not twitter_retriever.is_favorite
