from os import path, makedirs
from os.path import sep

from app.twitter_learning_journal.builders.cache_path_builder import build_cache_path, tweet_cache_path
from app.twitter_learning_journal.services.pickle_service import write_pickle_data, load_pickle_data


class Cacher:
    def __init__(self, entity, entity_id, *, sub_directory: str = '', cache_type: str = tweet_cache_path):
        self.entity = entity
        self.entity_id = entity_id
        self.sub_directory = sub_directory
        self.cache_type = cache_type

        entity_path = f'{sep}{entity_id}' if entity_id else ''

        self.cache_path = build_cache_path(cache_type=cache_type, sub_directory=sub_directory)
        self.file_path = f'{self.cache_path}{entity_path}'

        self._init_cache_dir()

    def is_cached(self):
        return path.isfile(self.file_path)

    def cache(self):
        write_pickle_data(self.entity, self.file_path)

    def get(self):
        return load_pickle_data(self.file_path)

    def _init_cache_dir(self):
        if not path.isdir(self.cache_path):
            makedirs(self.cache_path)
