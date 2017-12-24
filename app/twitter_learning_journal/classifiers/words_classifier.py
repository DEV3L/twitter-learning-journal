from collections import Counter

from app.twitter_learning_journal.classifiers.word_classifier import WordClassifier


class WordsClassifier:
    def __init__(self, words: list, classification_model: dict, *, weight=1):
        self.words = words
        self.classification_model = classification_model
        self.weight = weight

    def classify(self) -> Counter:
        classification = Counter()

        for word in self.words:
            _word = word.lower()
            word_classifier = WordClassifier(_word, self.classification_model, weight=self.weight)
            classification += word_classifier.classify()

        return classification
