from app.twitter_learning_journal.builders.cache_path_builder import webpage_cache_path
from app.twitter_learning_journal.cachers.cacher import Cacher
from app.twitter_learning_journal.transformers.transform_str import sha_str


class WebpageCacher(Cacher):
    def __init__(self, url: str, *, raw_data=None):
        self.url = url
        self.sha_url = sha_str(url)

        super().__init__(raw_data, self.sha_url, cache_type=webpage_cache_path)
