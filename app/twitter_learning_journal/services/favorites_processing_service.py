from app.twitter_learning_journal.classifiers import get_classification_model
from app.twitter_learning_journal.classifiers.favorite_classifier import FavoriteClassifier
from app.twitter_learning_journal.transformers.transform_str import remove_ignore_characters_from_str


class FavoritesProcessingService:
    def __init__(self, favorites: list, *, classification_model=None, weight_text=1, weight_hashtag=3):
        # reference to global static state... not ideal
        self.classification_model = get_classification_model(classification_model)
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
            FavoriteClassifier(favorite, classification_model=self.classification_model).classify()


def count_tokens(input_str):
    return int(len(input_str.split()))
