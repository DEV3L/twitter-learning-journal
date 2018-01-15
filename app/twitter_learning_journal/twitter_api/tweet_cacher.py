from app.twitter_learning_journal.dao.os_env import os_environ
from app.twitter_learning_journal.models.tweet import Tweet

tweet_cache_path = os_environ('TWEET_CACHE_PATH', default='./data/pickle/tweets/')


class TweetCacher:
    def __init__(self, tweet: Tweet):
        self.cache_path = tweet_cache_path
        self.tweet = tweet
