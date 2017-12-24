from pytest import mark

from app.twitter_learning_journal.classifiers.words_classifier import WordsClassifier
from tests.twitter_learning_journal import test_classification_model


@mark.parametrize("tag_count, not_tag_count, words, weight", [
    (0, 0, [], 1),
    (1, 0, ['tag'], 1),
    (1, 0, ['Tag'], 1),
    (2, 0, ['tag', 'tag'], 1),
    (1, 1, ['tag', 'not_tag'], 1),
    (0, 0, ['tagz'], 1),
    (2, 2, ['tag', 'not_tag'], 2),
])
def test_words_classifier_with_words(tag_count, not_tag_count, words, weight):
    expected_classification = {}

    if tag_count:
        expected_classification['tag'] = tag_count

    if not_tag_count:
        expected_classification['not_tag'] = not_tag_count

    words_classifier = WordsClassifier(words, test_classification_model, weight=weight)
    classification = words_classifier.classify()
    assert expected_classification == classification
