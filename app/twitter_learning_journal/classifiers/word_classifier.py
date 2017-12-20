from collections import defaultdict


class WordClassifier:
    def __init__(self, word: str, classification_model: dict):
        self.word = word
        self.classification_model = classification_model

    def classify(self) -> defaultdict(int):
        word_classification = defaultdict(int)
        for key, classifications in self.classification_model.items():
            word_classification[key] += self.word in classifications

        return word_classification
