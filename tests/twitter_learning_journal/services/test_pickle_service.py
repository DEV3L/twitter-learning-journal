from unittest.mock import patch

from app.twitter_learning_journal.services.pickle_service import load_pickle_data


@patch('app.twitter_learning_journal.services.pickle_service.open')
@patch('app.twitter_learning_journal.services.pickle_service.pickle')
def test_load_pickle_data(mock_pickle, mock_open):
    expected_unpickled_object = mock_pickle.load.return_value

    unpickled_object = load_pickle_data('path')

    assert expected_unpickled_object == unpickled_object
    mock_open.assert_called_with('path', 'rb')
    mock_pickle.load.assert_called_with(mock_open.return_value)
