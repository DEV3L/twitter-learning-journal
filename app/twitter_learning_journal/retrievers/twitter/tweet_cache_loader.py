from pathlib import Path

from app.twitter_learning_journal.cachers.cacher import Cacher
from app.twitter_learning_journal.services.pickle_service import load_pickle_data


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

    @staticmethod
    def _load_cached_tweet(file):
        tweet = load_pickle_data(file)
        return tweet
