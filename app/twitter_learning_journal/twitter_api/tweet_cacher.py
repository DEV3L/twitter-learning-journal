import pickle
from os import makedirs, path

from app.twitter_learning_journal.builders.cache_path_builder import build_cache_path
from app.twitter_learning_journal.models.tweet import Tweet
from app.twitter_learning_journal.services.pickle_service import load_pickle_data


class TweetCacher:
    def __init__(self, screen_name: str, tweet: Tweet):
        self.cache_path = build_cache_path(screen_name)
        self.tweet = tweet
        self.file_path = f'{self.cache_path}{tweet.id}'

        self._init_cache_dir()

    def is_cached(self):
        return path.isfile(self.file_path)

    def cache(self):
        pickle.dump(self.tweet, open(self.file_path, 'wb'))

    def get(self):
        return load_pickle_data(self.file_path)

    def _init_cache_dir(self):
        if not path.isdir(self.cache_path):
            makedirs(self.cache_path)
