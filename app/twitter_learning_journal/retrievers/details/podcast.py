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
        podcasts = [detail for detail in self.details
                    if 'pca.st' in detail.url or
                    'listened to' in detail.tweet.full_text.lower() or
                    'listend to' in detail.tweet.full_text.lower()]
        return podcasts

    def classify(self):
        podcasts = self.podcasts

        for detail in podcasts:
            full_text = detail.tweet.full_text
            full_text = full_text \
                .replace('@AgileUprising\nPodcast', '@AgileUprising Podcast') \
                .replace('@AgileUprising', 'Agile Uprising')

            if 'listened to' in full_text.lower() \
                    or 'listend to' in full_text.lower():
                title = ':'.join(full_text.split('\n')[0].split(':')[1:]).strip()
                detail.title = title

            minutes = self.podcast_default_minutes
            counter = [line for line in full_text.split('\n') if line.startswith('^')]

            if counter:
                counter_str = counter[0]
                try:
                    minutes = int(counter_str[1:].replace('m', ''))
                except:
                    pass

            detail.type = 'podcast'

            for url in detail.url.split('|'):
                # auto extraction to be implemented
                if url in podcast_urls_and_times:
                    minutes = podcast_urls_and_times[url]

            detail.count = minutes

            if self.podcast_default_minutes == minutes:
                logger.warning(f'Default time on podcast:{detail.id} - {detail.title}')
            else:
                detail.is_fully_classified = True


# manually extracted times predates count ^ identifier
podcast_urls_and_times = {
    'https://ryanripley.com/afh-074-the-past-present-future-of-scrum/': 76,
    'http://pca.st/up86': 70,
    'http://pca.st/8Y4G': 75,
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
    'http://pca.st/8TLM': 21,
    'http://pca.st/uRCi': 50,
    'http://pca.st/q9RK': 57,
    'http://pca.st/nN91': 62,
    'http://pca.st/7037': 39
}
