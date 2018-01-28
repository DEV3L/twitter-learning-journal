from pytest import mark

from app.twitter_learning_journal.classifiers import ignore_characters
from app.twitter_learning_journal.transformers.transform_str import remove_ignore_characters_from_str, tokenize, sha_str


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


@mark.parametrize('expected_value, value', [
    ('da39a3ee5e6b4b0d3255bfef95601890afd80709', ''),
    ('b858cb282617fb0956d960215c8e84d1ccf909c6', ' '),
    ('a94a8fe5ccb19ba61c4c0873d391e987982fbbd3', 'test'),
])
def test_sha_str(expected_value, value):
    assert expected_value == sha_str(value)
