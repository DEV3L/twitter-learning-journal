from collections import defaultdict


class WordClassifier:
    def __init__(self, word, classification_model):
        self.word = word
        self.classification_model = classification_model

    def classify(self):
        word_classification = defaultdict(int)
        for key, classifications in self.classification_model.items():
            word_classification[key] += self.word in classifications

        return word_classification
