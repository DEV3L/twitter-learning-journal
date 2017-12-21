from pytest import mark

from app.twitter_learning_journal.models.favorite import Favorite
from app.twitter_learning_journal.services.favorites_processing_service import FavoritesProcessingService
from tests.twitter_learning_journal import test_classification_model


def test_favorites_processing_service_init():
    favorites = []
    favorites_processing_service = FavoritesProcessingService(favorites)

    assert favorites == favorites_processing_service.favorites


def test_count_words_in_favorites():
    favorites = [
        Favorite(full_text='word'),
        Favorite(full_text='word\nword'),
        Favorite(full_text=' wor''d. , ! * ( ) = + ` ~ " '' word word'),
    ]

    favorites_processing_service = FavoritesProcessingService(favorites)
    favorites_processing_service.count_words_in_favorites()

    assert 6 == sum([favorite.word_count for favorite in favorites])


@mark.parametrize("expected_classification_values, hashtags, full_texts",
                  [  # expected_classification_values, hashtags, full_text
                      ([''], [''], [None, ]),
                      (['tag'], ['tag'], [None]),
                      (['tag', ''], ['tag', 'tagz'], [None, None]),
                      (['tag', ''], ['tag', 'tagz'], [None, None]),
                      (['tag', 'tag'], ['tag|tags', 'tag'], [None, None]),
                      (['tag'], ['tag|not_tag'], [None]),
                      ([''], ['tagz'], [None]),
                      (['tag'], [''], ['tag']),
                      (['tag'], ['tag'], ['not tag']),
                      (['not_tag'], ['tag'], ['not_tag not_tag']),
                  ])
def test_classify_favorites(expected_classification_values, hashtags, full_texts):
    favorites = [Favorite(hashtags=hashtag, full_text=full_text)
                 for hashtag, full_text in zip(hashtags, full_texts)]
    favorites_processing_service = FavoritesProcessingService(favorites, classification_model=test_classification_model)

    favorites_processing_service.classify_favorites()

    for count, expected_classification_value in enumerate(expected_classification_values):
        assert expected_classification_value == favorites_processing_service.favorites[count].classification
