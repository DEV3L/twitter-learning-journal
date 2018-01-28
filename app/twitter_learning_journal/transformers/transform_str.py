import hashlib

from app.twitter_learning_journal.classifiers import ignore_characters


def remove_ignore_characters_from_str(input_str, replacement=' '):
    if not input_str:
        return input_str

    for ignore_character in ignore_characters:
        input_str = input_str.replace(ignore_character, replacement)
    return input_str


def tokenize(input_str, *, delimiter=None):
    return input_str.split(delimiter) if input_str else []


def sha_str(input_str):
    hash_object = hashlib.sha1(input_str.encode())
    return hash_object.hexdigest()
