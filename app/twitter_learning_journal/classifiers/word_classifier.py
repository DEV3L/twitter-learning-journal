from collections import defaultdict, Counter


class WordClassifier:
    def __init__(self, word: str, classification_model: dict, *, weight: int = 1):
        self.word = word
        self.classification_model = classification_model
        self.weight = weight

    def classify(self) -> defaultdict(int):
        word_classification = defaultdict(int)
        for key, classifications in self.classification_model.items():
            word_classification[key] += (self.word in classifications) * self.weight

        return Counter(word_classification)
