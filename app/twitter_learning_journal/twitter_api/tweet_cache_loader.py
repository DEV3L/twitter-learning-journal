import os
from pathlib import Path

from app.twitter_learning_journal.builders.cache_path_builder import build_cache_path
from app.twitter_learning_journal.services.pickle_service import load_pickle_data


class TweetCacheLoader:
    def __init__(self, screen_name):
        self.screen_name = screen_name
        self.cache_path = build_cache_path(screen_name)

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
