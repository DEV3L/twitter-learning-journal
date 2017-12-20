from collections import Counter

from app.twitter_learning_journal.classifiers.word_classifier import WordClassifier


class WordsClassifier:
    def __init__(self, words: list, classification_model: dict):
        self.words = words
        self.classification_model = classification_model

    def classify(self) -> Counter:
        classification = Counter()

        for word in self.words:
            word_classifier = WordClassifier(word, self.classification_model)
            word_classification = Counter(word_classifier.classify())
            classification += word_classification

        return classification
