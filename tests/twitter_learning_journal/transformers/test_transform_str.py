from app.twitter_learning_journal.classifiers import ignore_characters
from app.twitter_learning_journal.transformers.transform_str import remove_ignore_characters_from_str, tokenize


def test_remove_ignore_characters_from_str():
    for character in ignore_characters:
        assert ' ' == remove_ignore_characters_from_str(character)


def test_remove_ignore_characters_from_str_with_replacement():
    replacement = '|'
    for character in ignore_characters:
        assert replacement == remove_ignore_characters_from_str(character, replacement=replacement)


def test_tokenize():
    test_cases = [
        ('', None, []),
        (' ', None, []),
        ('a b', None, ['a', 'b']),
        ('a|b', '|', ['a', 'b']),
    ]

    for input_str, delimiter, expected_value in test_cases:
        assert expected_value == tokenize(input_str, delimiter=delimiter)
