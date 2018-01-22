from app.twitter_learning_journal.dao.tweet_dao import TweetDao
from app.twitter_learning_journal.retrievers.twitter.api import get_api
from app.twitter_learning_journal.retrievers.twitter.tweets import Tweets


class TwitterRetriever():
    def __init__(self, tweet_dao: TweetDao, screen_name: str):
        self.api = get_api()
        self.tweet_dao = tweet_dao
        self.screen_name = screen_name

    def fetch(self):
        retrieved_tweets = []
        retrieved_tweets.extend(self._fetch('tweet'))
        retrieved_tweets.extend(self._fetch('favorite'))

        # should only save non-cached tweets
        self._save_tweets(retrieved_tweets)

        return retrieved_tweets

    def _fetch(self, tweet_type):
        tweets = Tweets(self.api, self.screen_name, tweet_type=tweet_type)
        return tweets.get()

    def _save_tweets(self, tweets: list):
        for tweet in tweets:
            if not self.tweet_dao.exists(tweet.id):
                self.tweet_dao.add(tweet)

        self.tweet_dao.commit()
