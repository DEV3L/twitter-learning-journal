from tweepy import API

from app.twitter_learning_journal.dao.tweet_dao import TweetDao
from app.twitter_learning_journal.retrievers.twitter.tweets import Tweets


class TwitterRetriever():
    def __init__(self, api: API, tweet_dao: TweetDao, screen_name: str, is_favorite: bool = False):
        self.api = api
        self.tweet_dao = tweet_dao
        self.screen_name = screen_name
        self.is_favorite = is_favorite
        self._tweet_type = 'favorite' if is_favorite else 'tweet'

    def fetch(self):
        tweets = Tweets(self.api, self.screen_name, tweet_type=self._tweet_type)

        retrieved_tweets = tweets.get()
        self.save_tweets(retrieved_tweets)

        return retrieved_tweets

    def save_tweets(self, tweets: list):
        for tweet in tweets:
            if not self.tweet_dao.exists(tweet.id):
                self.tweet_dao.add(tweet)

        self.tweet_dao.commit()
