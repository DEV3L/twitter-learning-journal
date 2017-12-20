from app.twitter_learning_journal.classifiers import ignore_characters
from app.twitter_learning_journal.transformers.transform_str import remove_ignore_characters_from_str


def test_remove_ignore_characters_from_str():
    for character in ignore_characters:
        assert ' ' == remove_ignore_characters_from_str(character)


def test_remove_ignore_characters_from_str_with_replacement():
    replacement = '|'
    for character in ignore_characters:
        assert replacement == remove_ignore_characters_from_str(character, replacement=replacement)
