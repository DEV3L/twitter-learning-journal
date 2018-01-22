from app.twitter_learning_journal.services.tweets_processing_service import TweetsProcessingService


class TweetsClassifier():
    def __init__(self, tweets: list):
        self.tweets = tweets

    def classify(self):
        tweets_processing_service = TweetsProcessingService(self.tweets)
        tweets_processing_service.count_tweet_words()
        tweets_processing_service.classify_tweets()
        tweets_processing_service.sub_classify_unclassified_tweets()
