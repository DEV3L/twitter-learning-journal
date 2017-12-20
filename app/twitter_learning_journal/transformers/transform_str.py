from app.twitter_learning_journal.classifiers import ignore_characters


def remove_ignore_characters_from_str(input_str, replacement=' '):
    for ignore_character in ignore_characters:
        input_str = input_str.replace(ignore_character, replacement)
    return input_str
