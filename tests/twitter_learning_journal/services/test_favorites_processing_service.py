from app.twitter_learning_journal.models.favorite import Favorite
from app.twitter_learning_journal.services.favorites_processing_service import FavoritesProcessingService


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


classification_model = {
    'tag': {'tag'},
    'not_tag': {'not_tag'}
}

favorites = [
    Favorite(full_text='not_tag'),
    Favorite(full_text='tag'),
    Favorite(full_text='tag not_tag'),
    Favorite(full_text='tag tag other_tag'),
    Favorite(full_text='tag other_tag'),
]
