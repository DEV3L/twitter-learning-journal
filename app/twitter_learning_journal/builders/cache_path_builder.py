from app.twitter_learning_journal.dao.os_env import os_environ

pickle_cache_path = os_environ('CACHE_PATH', default='./data/pickle/')
webpage_cache_path = os_environ('WEBPAGE_CACHE_PATH', default=f'{pickle_cache_path}web_pages/')
tweet_cache_path = os_environ('TWEET_CACHE_PATH', default=f'{pickle_cache_path}tweets/')


def build_cache_path(cache_type=tweet_cache_path, sub_directory=''):
    return f'{cache_type}{sub_directory}'
