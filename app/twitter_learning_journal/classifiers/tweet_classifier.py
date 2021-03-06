from collections import Counter

from app.twitter_learning_journal.classifiers import get_classification_model
from app.twitter_learning_journal.classifiers.words_classifier import WordsClassifier
from app.twitter_learning_journal.models.tweet import Tweet
from app.twitter_learning_journal.transformers.transform_dict import transform_dict_into_keys_sorted_by_value
from app.twitter_learning_journal.transformers.transform_str import tokenize, remove_ignore_characters_from_str


class TweetClassifier():
    def __init__(self, tweet: Tweet, *, classification_model=None, weight_text=1, weight_hashtag=3):
        self.classification_model = get_classification_model(classification_model)
        self.tweet = tweet
        self.weight_text = weight_text
        self.weight_hashtag = weight_hashtag

    def classify(self):
        hashtag_classification = self._classify_hashtags()
        full_text_classification = self._classify_full_text()

        classification = hashtag_classification
        classification += full_text_classification

        classification_value = _extract_classification(classification)

        self.tweet.classification = classification_value

    def _classify_hashtags(self) -> Counter:
        return self._classify_words(self.tweet.hashtags, self.weight_hashtag, delimiter='|')

    def _classify_full_text(self) -> Counter:
        return self._classify_words(self.tweet.full_text, self.weight_text)

    def _classify_words(self, words, weight, *, delimiter=' '):
        if delimiter is None:
            words = tokenize(remove_ignore_characters_from_str(words), delimiter=delimiter)
        else:
            _words = words.split(delimiter) if words else []
            words = tokenize(delimiter.join([remove_ignore_characters_from_str(word) for word in _words]),
                             delimiter=delimiter)

        words_classifier = WordsClassifier(words, self.classification_model, weight=weight)
        return words_classifier.classify()


def _extract_classification(classification):
    sorted_keys = transform_dict_into_keys_sorted_by_value(classification, reverse=True)
    return sorted_keys[0] if sorted_keys else ''
