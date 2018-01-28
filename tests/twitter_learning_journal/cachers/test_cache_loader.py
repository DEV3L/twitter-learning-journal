from unittest.mock import patch, MagicMock

from pytest import fixture

from app.twitter_learning_journal.cachers.cache_loader import CacheLoader

expected_cache_path = './data/pickle/tweets/screen name'
expected_screen_name = 'screen name'


@fixture(name='cache_loader')
@patch('app.twitter_learning_journal.cachers.cache_loader.Cacher._init_cache_dir')
def _cache_loader(mock_init_cache_dir):
    cache_loader = CacheLoader(expected_screen_name)
    assert mock_init_cache_dir.called
    return cache_loader


def test_cache_loader_init(cache_loader):
    assert expected_screen_name == cache_loader.sub_directory
    assert expected_cache_path == cache_loader.cache_path


@patch('app.twitter_learning_journal.cachers.cache_loader.load_pickle_data')
def test_load_cached_entity(mock_load_pickle_data, cache_loader):
    expected_file_path = 'test'
    expected_entity = mock_load_pickle_data.return_value

    tweet = cache_loader.load_cached_entity('test')

    assert expected_entity == tweet
    mock_load_pickle_data.assert_called_with(f'{cache_loader.cache_path}{expected_file_path}')


@patch('app.twitter_learning_journal.cachers.cache_loader.Path')
def test_load_cached_entitys(mock_path, cache_loader):
    _object = 'test'
    expected_cached_entitys = [_object]

    mock_load_cached_entity = MagicMock()
    mock_load_cached_entity.return_value = _object
    cache_loader.load_cached_entity = mock_load_cached_entity

    mock_cache_dir = MagicMock()
    mock_cache_dir.iterdir.return_value = [_object]

    mock_path.return_value = mock_cache_dir

    cached_entities = cache_loader.load_cached_entities()

    assert expected_cached_entitys == cached_entities
    mock_load_cached_entity.assert_called_with(_object)
    mock_path.assert_called_with(cache_loader.cache_path)
