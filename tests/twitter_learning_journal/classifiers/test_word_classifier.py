from app.twitter_learning_journal.classifiers.word_classifier import WordClassifier


def test_word_classifier_init():
    word = 'word'

    classification_model = {
        'tag': [word],
        'not tag': [word, 'not word'],
        'gat': [],
        'not gat': ['not word', 'Word'],
    }

    expected_classification = {
        'tag': 1,
        'not tag': 1,
        'gat': 0,
        'not gat': 0
    }

    word_classifier = WordClassifier(word, classification_model)
    classification = word_classifier.classify()

    assert expected_classification == classification
