from unittest.mock import MagicMock, patch

from pytest import mark

from app.twitter_learning_journal.classifiers import global_classification_model
from app.twitter_learning_journal.classifiers.favorite_classifier import FavoriteClassifier, _extract_classification
from app.twitter_learning_journal.models.favorite import Favorite
from tests.twitter_learning_journal import test_classification_model


def test_favorite_classifier_init():
    favorite = Favorite()
    favorite_classifier = FavoriteClassifier(favorite)

    assert favorite == favorite_classifier.favorite
    assert global_classification_model == favorite_classifier.classification_model

    favorite_classifier = FavoriteClassifier(favorite, classification_model=test_classification_model)

    assert favorite == favorite_classifier.favorite
    assert test_classification_model == favorite_classifier.classification_model


@mark.parametrize('hashtags, full_text, expected_classification',
                  [
                      (None, None, ''),
                      ('', '', ''),
                      ('tag', '', 'tag'),
                      ('', 'tag', 'tag'),
                      ('tag', 'not_tag', 'tag'),
                      ('not_tag', 'tag', 'not_tag'),
                      ('tagz', 'tagz', ''),
                      ('tag', 'tag', 'tag'),
                  ])
def test_classify(hashtags, full_text, expected_classification):
    favorite = Favorite(hashtags=hashtags, full_text=full_text)
    favorite_classifier = FavoriteClassifier(favorite, classification_model=test_classification_model)
    favorite_classifier.classify()

    assert expected_classification == favorite.classification


@mark.parametrize('tag_count, not_tag_count, words, delimiter',
                  [
                      (0, 0, '', None),
                      (1, 0, 'tag', None),
                      (1, 0, 'tag tags', None),
                      (1, 1, 'tag not_tag', None),
                      (0, 0, 'tagz', None),
                  ])
def test_classify_words_(tag_count, not_tag_count, words, delimiter):
    expected_classification = {}

    if tag_count:
        expected_classification['tag'] = tag_count

    if not_tag_count:
        expected_classification['not_tag'] = not_tag_count

    favorite_classifier = FavoriteClassifier(Favorite(), classification_model=test_classification_model)
    classification = favorite_classifier._classify_words(words, delimiter=delimiter)
    assert expected_classification == classification


@patch('app.twitter_learning_journal.classifiers.favorite_classifier.FavoriteClassifier._classify_words')
def test_classify_hashtags(mock_classify_words):
    mock_favorite = MagicMock()
    favorite_classifier = FavoriteClassifier(mock_favorite, classification_model=test_classification_model)

    classified_hashtags = favorite_classifier._classify_hashtags()

    assert mock_classify_words.return_value == classified_hashtags
    mock_classify_words.assert_called_with(mock_favorite.hashtags, delimiter='|')


@patch('app.twitter_learning_journal.classifiers.favorite_classifier.FavoriteClassifier._classify_words')
def test_classify_full_text(mock_classify_words):
    mock_favorite = MagicMock()
    favorite_classifier = FavoriteClassifier(mock_favorite, classification_model=test_classification_model)

    classified_full_text = favorite_classifier._classify_full_text()

    assert mock_classify_words.return_value == classified_full_text
    mock_classify_words.assert_called_with(mock_favorite.full_text)


@mark.parametrize('classification, expected_value',
                  [
                      ({}, ''),
                      ({'a': 1, 'b': 2}, 'b'),
                      ({'a': 2, 'b': 2}, 'a'),
                  ])
def test_extract_classification(classification, expected_value):
    assert expected_value == _extract_classification(classification)
