from datetime import datetime
from unittest.mock import MagicMock, patch

from pytest import fixture

from app.twitter_learning_journal.models.favorite import Favorite
from app.twitter_learning_journal.twitter_api.favorites import Favorites


@fixture(name='favorites')
def _favorites():
    mock_twitter_api = MagicMock()
    favorites = Favorites(mock_twitter_api, 'screen_name')

    assert favorites
    assert mock_twitter_api == favorites._twitter_api
    assert 'screen_name' == favorites.screen_name

    return favorites


@patch('app.twitter_learning_journal.twitter_api.favorites.Cursor')
def test_call(mock_cursor, favorites):
    mock_cursor.return_value.items.return_value = ['1']

    generator_response = favorites._call()
    items = [item for item in generator_response]

    assert "<class 'generator'>" == str(type(generator_response))
    assert ['1'] == items
    assert mock_cursor.called
    mock_cursor.assert_called_with(favorites._twitter_api.favorites, 'screen_name', count=200, tweet_mode='extended')


@patch('app.twitter_learning_journal.twitter_api.favorites.Favorites._call')
def test_get(mock_call, favorites):
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
        ]
    }

    favorite_response = MagicMock(id=id, created_at=created_at, full_text=full_text, entities=entities)
    expected_favorite_model = Favorite(
        id=id,
        created_at=created_at,
        full_text=full_text,
        hashtags='some_text|other_text'
    )

    mock_call.return_value = [favorite_response]

    favorites_list = favorites.get()

    assert [expected_favorite_model] == favorites_list
    assert mock_call.called
    # mock_json.dumps.assert_called_with(mock_like._json)
