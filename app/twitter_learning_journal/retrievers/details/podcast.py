from app.twitter_learning_journal.services.logging_service import LoggingService

logger = LoggingService('Podcasts')


class PodcastExtractor:
    podcast_default_minutes = 20

    def __init__(self, details):
        self._details = details

    @property
    def details(self):
        details = [detail for detail in self._details if detail.url]
        return details

    @property
    def podcasts(self):
        # share url from pocket cast has 'pca.st' in it
        podcasts = [detail for detail in self.details if 'pca.st' in detail.url]
        return podcasts

    def classify(self):
        podcasts = self.podcasts

        for detail in podcasts:
            detail.type = 'podcast'
            minutes = self.podcast_default_minutes

            for url in detail.url.split('|'):
                # auto extraction to be implemented
                if url in podcast_urls_and_times:
                    minutes = podcast_urls_and_times[url]
                    detail.is_fully_classified = True
                else:
                    logger.warning(f'Podcast url: {url} not mapped')

            detail.count = minutes


# manually extracted times predates count ^ identifier
podcast_urls_and_times = {
    'http://pca.st/Z0Kh': 42,
    'http://pca.st/9GMB': 78,
    'http://pca.st/Ha6R': 49,
    'http://pca.st/xJ9C': 66,
    'http://pca.st/Rx7b': 50,
    'http://pca.st/fp1m': 59,
    'http://pca.st/l0il': 59,
    'http://pca.st/X8me': 54,
    'http://pca.st/shSo': 48,
    'http://pca.st/Lc6p': 25,
    'http://pca.st/H4Ym': 56,
    'http://pca.st/7zSP': 30,
    'http://pca.st/8TLM': 20,
    'http://pca.st/uRCi': 50,
    'http://pca.st/q9RK': 57,
    'http://pca.st/nN91': 62,
    'http://pca.st/7037': 39
}
