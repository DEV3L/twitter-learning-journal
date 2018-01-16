import os
from pathlib import Path

from app.twitter_learning_journal.services.pickle_service import load_pickle_data
from app.twitter_learning_journal.twitter_api.cacher import Cacher


class TweetCacheLoader(Cacher):
    def __init__(self, screen_name):
        super().__init__(screen_name)

    def load_cached_tweets(self):
        tweets = []

        cache_dir = Path(self.cache_path)
        for file in cache_dir.iterdir():
            tweet = self._load_cached_tweet(file)
            tweets.append(tweet)

        return tweets

    def _load_cached_tweet(self, file):
        file_path = f'{self.cache_path}{os.sep}{file}'
        tweet = load_pickle_data(file_path)
        return tweet
