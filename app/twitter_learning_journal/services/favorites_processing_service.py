class FavoritesProcessingService:
    def __init__(self, favorites: list):
        self.favorites = favorites

    def count_words(self):
        for favorite in self.favorites:
            _full_text = favorite.full_text
            for ignore_character in ignore_characters:
                _full_text = _full_text.replace(ignore_character, ' ')

            word_count = len(_full_text.split())
            favorite.word_count = word_count


ignore_characters = [
    '.',
    ',',
    '!',
    '*',
    '(',
    ')',
    '=',
    '+',
    '`',
    '~',
    '"',
    "'"
]
