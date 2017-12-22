from app.twitter_learning_journal.classifiers import get_classification_model
from app.twitter_learning_journal.classifiers.tweet_classifier import TweetClassifier
from app.twitter_learning_journal.transformers.transform_str import remove_ignore_characters_from_str


class TweetsProcessingService:
    def __init__(self, tweets: list, *, classification_model=None, weight_text=1, weight_hashtag=3):
        # reference to global static state... not ideal
        self.classification_model = get_classification_model(classification_model)
        self.tweets = tweets
        self.weight_text = weight_text
        self.weight_hashtag = weight_hashtag

    def count_tweet_words(self):
        for tweet in self.tweets:
            _full_text = remove_ignore_characters_from_str(tweet.full_text)
            word_count = count_tokens(_full_text)
            tweet.word_count = word_count

    def classify_tweets(self):
        for tweet in self.tweets:
            TweetClassifier(tweet, classification_model=self.classification_model).classify()


def count_tokens(input_str):
    return int(len(input_str.split()))
