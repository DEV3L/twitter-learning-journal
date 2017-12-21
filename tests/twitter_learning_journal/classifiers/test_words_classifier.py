from pytest import mark

from app.twitter_learning_journal.classifiers.words_classifier import WordsClassifier
from tests.twitter_learning_journal import test_classification_model

test_cases = [
    # (tag_count, not_tag_count, words),
    (0, 0, []),
    (1, 0, ['tag']),
    (1, 0, ['Tag']),
    (2, 0, ['tag', 'tag']),
    (1, 1, ['tag', 'not_tag']),
    (0, 0, ['tagz']),
]


@mark.parametrize("tag_count, not_tag_count, words", test_cases)
def test_words_classifier_with_words(tag_count, not_tag_count, words):
    expected_classification = {}

    if tag_count:
        expected_classification['tag'] = tag_count

    if not_tag_count:
        expected_classification['not_tag'] = not_tag_count

    words_classifier = WordsClassifier(words, test_classification_model)
    classification = words_classifier.classify()
    assert expected_classification == classification
