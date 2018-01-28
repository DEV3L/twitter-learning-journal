from unittest.mock import patch

from app.twitter_learning_journal.builders.cache_path_builder import webpage_cache_path
from app.twitter_learning_journal.cachers.webpage_cacher import WebpageCacher


@patch('app.twitter_learning_journal.cachers.tweet_cacher.Cacher._init_cache_dir')
def test_webpage_cacher_init(mock_init_cache_dir):
    expected_url = 'http://www.domain.com/'
    expected_sha_url = '6298c286a5fc073cf4d30b0157cce6eaf133c031'
    expected_raw_data = b'raw_data'
    expected_webpage_cache_path = webpage_cache_path

    webpage_cacher = WebpageCacher(expected_url, raw_data=expected_raw_data)

    assert expected_sha_url == webpage_cacher.sha_url
    assert expected_sha_url == webpage_cacher.entity_id
    assert expected_url == webpage_cacher.url
    assert expected_raw_data == webpage_cacher.entity
    assert expected_webpage_cache_path == webpage_cacher.cache_path
    assert mock_init_cache_dir.called
