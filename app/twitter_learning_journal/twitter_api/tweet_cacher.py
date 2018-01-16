from os import path

from app.twitter_learning_journal.models.tweet import Tweet
from app.twitter_learning_journal.services.pickle_service import load_pickle_data, write_pickle_data
from app.twitter_learning_journal.twitter_api.cacher import Cacher


class TweetCacher(Cacher):
    def __init__(self, screen_name: str, tweet: Tweet):
        super().__init__(screen_name)
        self.tweet = tweet
        self.file_path = f'{self.cache_path}{tweet.id}'

    def is_cached(self):
        return path.isfile(self.file_path)

    def cache(self):
        write_pickle_data(self.tweet, self.file_path)

    def get(self):
        return load_pickle_data(self.file_path)
