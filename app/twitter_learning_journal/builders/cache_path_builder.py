from app.twitter_learning_journal.dao.os_env import os_environ

tweet_cache_path = os_environ('TWEET_CACHE_PATH', default='./data/pickle/tweets/')


def build_cache_path(screen_name):
    return f'{tweet_cache_path}{screen_name}'
