from collections import Counter

from app.twitter_learning_journal.classifiers import global_classification_model
from app.twitter_learning_journal.classifiers.words_classifier import WordsClassifier
from app.twitter_learning_journal.transformers.transform_str import remove_ignore_characters_from_str


class FavoritesProcessingService:
    def __init__(self, favorites: list, *, classification_model=None, weight_text=1, weight_hashtag=3):
        # reference to global static state... not ideal
        self.classification_model = classification_model or global_classification_model
        self.favorites = favorites
        self.weight_text = weight_text
        self.weight_hashtag = weight_hashtag

    def count_words_in_favorites(self):
        for favorite in self.favorites:
            _full_text = remove_ignore_characters_from_str(favorite.full_text)
            word_count = count_tokens(_full_text)
            favorite.word_count = word_count

    def classify_favorites(self):
        for favorite in self.favorites:
            classification = Counter()

            hashtag_classification = self._classify_hashtags(favorite.hashtags)
            # full_text_classification = self._classify_full_text_in_favorites()

            classification += hashtag_classification
            # classification += full_text_classification
            classification_value = ''

            if classification:
                classification_value = sorted(hashtag_classification, key=hashtag_classification.get, reverse=True)[0]

            favorite.classification = classification_value

    def _classify_hashtags(self, hashtags) -> Counter:
        hashtags = hashtags.split('|')
        words_classifier = WordsClassifier(hashtags, self.classification_model)
        return words_classifier.classify()

def count_tokens(input_str):
    return int(len(input_str.split()))
