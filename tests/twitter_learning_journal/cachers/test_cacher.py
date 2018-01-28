from unittest.mock import patch

from app.twitter_learning_journal.cachers.cacher import Cacher

expected_cache_path = './data/pickle/tweets/screen name'
expected_screen_name = 'screen name'


@patch('app.twitter_learning_journal.cachers.cacher.makedirs')
@patch('app.twitter_learning_journal.cachers.cacher.path')
def test_init_cache_dir_exists(mock_path, mock_makedirs):
    mock_path.isdir.return_value = True

    cacher = Cacher(expected_screen_name, None, None)

    mock_path.isdir.assert_called_with(cacher.cache_path)
    assert not mock_makedirs.called


@patch('app.twitter_learning_journal.cachers.cacher.makedirs')
@patch('app.twitter_learning_journal.cachers.cacher.path')
def test_init_cache_dir_not_exists(mock_path, mock_makedirs):
    mock_path.isdir.return_value = False

    cacher = Cacher(expected_screen_name, None, None)

    mock_path.isdir.assert_called_with(cacher.cache_path)
    mock_makedirs.assert_called_with(cacher.cache_path)


@patch('app.twitter_learning_journal.cachers.cacher.path')
def test_is_cached(mock_path):
    expected_is_cached = True
    mock_path.isfile.return_value = expected_is_cached
    expected_file_path = f'{expected_cache_path}/1'

    cacher = Cacher(expected_screen_name, None, '1')

    is_cached = cacher.is_cached()

    assert expected_is_cached == is_cached
    mock_path.isfile.assert_called_with(expected_file_path)


@patch('app.twitter_learning_journal.cachers.cacher.path')
def test_is_not_cached(mock_path):
    expected_is_cached = False
    mock_path.isfile.return_value = expected_is_cached
    expected_file_path = f'{expected_cache_path}/1'

    cacher = Cacher(expected_screen_name, None, '1')

    is_cached = cacher.is_cached()

    assert expected_is_cached == is_cached
    mock_path.isfile.assert_called_with(expected_file_path)


@patch('app.twitter_learning_journal.cachers.cacher.write_pickle_data')
def test_cache(mock_write_pickle_data):
    cacher = Cacher(expected_screen_name, 'test', '1')

    cacher.cache()

    mock_write_pickle_data.assert_called_with('test', cacher.file_path)


@patch('app.twitter_learning_journal.cachers.cacher.load_pickle_data')
def test_get(mock_load_pickle_data):
    expected_entity = 'test'
    mock_load_pickle_data.return_value = expected_entity

    cacher = Cacher(expected_screen_name, 'test', '1')

    entity = cacher.get()

    assert expected_entity == entity
    mock_load_pickle_data.assert_called_with(cacher.file_path)
