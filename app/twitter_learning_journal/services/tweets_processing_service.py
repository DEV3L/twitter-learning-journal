from app.twitter_learning_journal.classifiers import get_classification_model
from app.twitter_learning_journal.classifiers.tweet_classifier import TweetClassifier
from app.twitter_learning_journal.transformers.transform_str import remove_ignore_characters_from_str


class TweetsProcessingService:
    sub_classification_factor = 10

    def __init__(self, tweets: list, *, classification_model=None,
                 weight_text: float = 1.0, weight_hashtag: float = 3.0):
        # reference to global static state... not ideal
        self.classification_model = get_classification_model(classification_model)
        self.tweets = tweets
        self.weight_text = weight_text
        self.weight_hashtag = weight_hashtag

    @property
    def sub_weight_text(self):
        return self.weight_text / self.sub_classification_factor

    @property
    def sub_weight_hashtag(self):
        return self.weight_hashtag / self.sub_classification_factor

    def count_tweet_words(self):
        for tweet in self.tweets:
            _full_text = remove_ignore_characters_from_str(tweet.full_text)
            word_count = count_tokens(_full_text)
            tweet.word_count = word_count

    def classify_tweets(self, *, is_sub_classify=False):
        [TweetClassifier(tweet, classification_model=self.classification_model).classify()
         for tweet in self.tweets]

        if is_sub_classify:
            self._sub_classify_tweets()

    def _sub_classify_tweets(self):
        sub_classification_model = self._create_sub_classification_model()

        unclassified_tweets = [tweet for tweet in self.tweets if not tweet.classification]
        tweets_processing_service = TweetsProcessingService(unclassified_tweets,
                                                            classification_model=sub_classification_model,
                                                            weight_text=self.sub_weight_text,
                                                            weight_hashtag=self.sub_weight_hashtag)
        tweets_processing_service.classify_tweets(is_sub_classify=False)

    def _create_sub_classification_model(self):
        classified_tweets = [tweet for tweet in self.tweets if tweet.classification]
        sub_classification_model = dict(get_classification_model(None))

        for tweet in classified_tweets:
            cleaned_full_text = remove_ignore_characters_from_str(tweet.full_text)
            updated_classification = sub_classification_model[tweet.classification].union(cleaned_full_text)
            sub_classification_model[tweet.classification] = updated_classification
        return sub_classification_model


def count_tokens(input_str):
    return int(len(input_str.split()))
