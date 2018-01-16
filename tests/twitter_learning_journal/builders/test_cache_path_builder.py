from app.twitter_learning_journal.builders.cache_path_builder import build_cache_path


def test_build_cache_path():
    expected_cache_path = './data/pickle/tweets/test'
    assert expected_cache_path == build_cache_path('test')
