from os import path, makedirs

from app.twitter_learning_journal.builders.cache_path_builder import build_cache_path


class Cacher:
    def __init__(self, screen_name: str):
        self.screen_name = screen_name
        self.cache_path = build_cache_path(screen_name)
        self._init_cache_dir()

    def _init_cache_dir(self):
        if not path.isdir(self.cache_path):
            makedirs(self.cache_path)
