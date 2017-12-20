from app.twitter_learning_journal.classifiers.words_classifier import WordsClassifier

classification_model = {
    'tag': {'tag', 'tags'},
    'not_tag': {'not_tag'}
}


def test_words_classifier_with_words():
    test_cases = (
        (0, 0, []),
        (1, 0, ['tag']),
        (2, 0, ['tag', 'tags']),
        (1, 1, ['tag', 'not_tag']),
        (0, 0, ['tagz']),
    )

    for tag_count, not_tag_count, words in test_cases:
        expected_classification = {}

        if tag_count:
            expected_classification['tag'] = tag_count

        if not_tag_count:
            expected_classification['not_tag'] = not_tag_count

        words_classifier = WordsClassifier(words, classification_model)
        classification = words_classifier.classify()
        assert expected_classification == classification
