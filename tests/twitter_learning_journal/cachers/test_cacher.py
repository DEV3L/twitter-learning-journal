from unittest.mock import patch

from app.twitter_learning_journal.cachers.cacher import Cacher

expected_screen_name = 'screen name'


@patch('app.twitter_learning_journal.cachers.cacher.makedirs')
@patch('app.twitter_learning_journal.cachers.cacher.path')
def test_init_cache_dir_exists(mock_path, mock_makedirs):
    mock_path.isdir.return_value = True

    cacher = Cacher(expected_screen_name)

    mock_path.isdir.assert_called_with(cacher.cache_path)
    assert not mock_makedirs.called


@patch('app.twitter_learning_journal.cachers.cacher.makedirs')
@patch('app.twitter_learning_journal.cachers.cacher.path')
def test_init_cache_dir_not_exists(mock_path, mock_makedirs):
    mock_path.isdir.return_value = False

    cacher = Cacher(expected_screen_name)

    mock_path.isdir.assert_called_with(cacher.cache_path)
    mock_makedirs.assert_called_with(cacher.cache_path)
