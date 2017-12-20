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


def test_classify_favorites():
    test_cases = (
        ([''], ['']),
        (['tag'], ['tag']),
        (['tag', ''], ['tag', 'tagz']),
        (['tag', 'tag'], ['tag|tags', 'tag']),
        (['tag'], ['tag|not_tag']),
        ([''], ['tagz']),
    )

    for expected_classification_values, hashtags in test_cases:
        favorites = [Favorite(hashtags=hashtag) for hashtag in hashtags]
        favorites_processing_service = FavoritesProcessingService(favorites, classification_model=classification_model)

        favorites_processing_service.classify_favorites()

        for count, expected_classification_value in enumerate(expected_classification_values):
            assert expected_classification_value == favorites_processing_service.favorites[count].classification


def test_classify_hashtags():
    test_cases = (
        (0, 0, ['']),
        (1, 0, ['tag']),
        (1, 0, ['tag|tags']),
        (1, 1, ['tag|not_tag']),
        (0, 0, ['tagz']),
    )

    for tag_count, not_tag_count, hashtags in test_cases:
        expected_classification = {}
        favorites = [Favorite(hashtags=hashtag) for hashtag in hashtags]

        if tag_count:
            expected_classification['tag'] = tag_count

        if not_tag_count:
            expected_classification['not_tag'] = not_tag_count

        favorites_processing_service = FavoritesProcessingService(favorites, classification_model=classification_model)

        for favorite in favorites:
            classification = favorites_processing_service._classify_hashtags(favorite.hashtags)

            assert expected_classification == classification


classification_model = {
    'tag': {'tag'},
    'not_tag': {'not_tag'}
}
