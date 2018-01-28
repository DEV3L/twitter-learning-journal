from pathlib import Path

from app.twitter_learning_journal.cachers.cacher import Cacher
from app.twitter_learning_journal.services.pickle_service import load_pickle_data


class CacheLoader(Cacher):
    def __init__(self, sub_directory):
        super().__init__(None, None, sub_directory=sub_directory)

    def load_cached_entities(self):
        entities = []

        cache_dir = Path(self.cache_path)
        for file in cache_dir.iterdir():
            entity = self.load_cached_entity(file, is_include_cache_path=False)
            entities.append(entity)

        return entities

    def load_cached_entity(self, file_name, *, is_include_cache_path=True):
        path = f'{self.cache_path}' if is_include_cache_path else ''
        entity = load_pickle_data(f'{path}{file_name}')
        return entity
