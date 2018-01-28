from pathlib import Path

from app.twitter_learning_journal.cachers.cacher import Cacher
from app.twitter_learning_journal.services.pickle_service import load_pickle_data


class CacheLoader(Cacher):
    def __init__(self, sub_directory):
        super().__init__(sub_directory, None, None)

    def load_cached_entities(self):
        entities = []

        cache_dir = Path(self.cache_path)
        for file in cache_dir.iterdir():
            entity = self.load_cached_entity(file)
            entities.append(entity)

        return entities

    def load_cached_entity(self, file_name):
        entity = load_pickle_data(f'{self.cache_path}{file_name}')
        return entity
