from app.twitter_learning_journal.dao.tweet_dao import TweetDao
from app.twitter_learning_journal.services.tweets_processing_service import TweetsProcessingService


class TweetsClassifier():
    def __init__(self, tweets: list, tweet_dao: TweetDao):
        self.tweets = tweets
        self.tweet_dao = tweet_dao

    def classify(self):
        tweets_processing_service = TweetsProcessingService(self.tweets)
        tweets_processing_service.count_tweet_words()
        tweets_processing_service.classify_tweets()
        tweets_processing_service.sub_classify_unclassified_tweets()

        self._save_tweets(tweets_processing_service.tweets)

    def _save_tweets(self, tweets):
        self.tweet_dao.add_all(tweets)
        self.tweet_dao.commit()
