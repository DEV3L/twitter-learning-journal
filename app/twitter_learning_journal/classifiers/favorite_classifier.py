from collections import Counter

from app.twitter_learning_journal.classifiers import get_classification_model
from app.twitter_learning_journal.classifiers.words_classifier import WordsClassifier
from app.twitter_learning_journal.models.favorite import Favorite


class FavoriteClassifier():
    def __init__(self, favorite: 'Favorite', *, classification_model=None):
        self.classification_model = get_classification_model(classification_model)
        self.favorite = favorite

    def classify(self):
        hashtag_classification = self._classify_hashtags()
        full_text_classification = self._classify_full_text()

        classification = hashtag_classification
        classification += full_text_classification

        classification_value = self.extract_classification(classification)

        self.favorite.classification = classification_value

    def _classify_hashtags(self) -> Counter:
        return self._classify_words(self.favorite.hashtags, delimiter='|')

    def _classify_full_text(self) -> Counter:
        return self._classify_words(self.favorite.full_text)

    def _classify_words(self, words, *, delimiter=None):
        words = tokenize(words, delimiter=delimiter)
        words_classifier = WordsClassifier(words, self.classification_model)
        return words_classifier.classify()

    def extract_classification(self, classification):
        if not classification:
            return ''
        return sorted(classification, key=classification.get, reverse=True)[0]


def tokenize(input_str, *, delimiter=None):
    return input_str.lower().split(delimiter) if input_str else []
