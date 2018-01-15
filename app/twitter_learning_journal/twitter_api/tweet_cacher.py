from app.twitter_learning_journal.dao.os_env import os_environ
from app.twitter_learning_journal.models.tweet import Tweet

tweet_cache_path = os_environ('TWEET_CACHE_PATH', default='./data/pickle/tweets/')

from os import makedirs, path

class TweetCacher:
    def __init__(self, screen_name: str, tweet: Tweet):
        self.cache_path = f'{tweet_cache_path}{screen_name}'
        self.tweet = tweet

        self._init_cache_dir()

    def _init_cache_dir(self):
        if not path.isdir(self.cache_path):
            makedirs(self.cache_path)
