from app.twitter_learning_journal.dao.tweet_dao import TweetDao
from app.twitter_learning_journal.database.sqlalchemy_database import Database
from app.twitter_learning_journal.models.detail import Detail


def count_podcast_words():
    database = Database(echo=False)
    tweet_dao = TweetDao(database)
    details = tweet_dao._database.query(Detail).all()

    # share url from pocket cast has 'pca.st' in it
    details = [detail for detail in details if detail.url and
               [url for url in detail.url.split('|') if 'pca.st' in url]
               ]

    for detail in details:
        if detail.is_fully_classified:
            continue

        detail.type = 'podcast'
        minutes = podcast_default_minutes

        for url in detail.url.split('|'):
            if 'pca.st' not in url:
                continue

            if url in podcast_urls_and_times:
                minutes = podcast_urls_and_times[url]
                detail.is_fully_classified = True
            else:
                detail.is_fully_classified = False
                print(url)

        detail.word_count = minutes * podcast_words_per_minute
        database.commit()


# https://www.quora.com/Speeches-For-the-average-person-speaking-at-a-normal-pace-what-is-the-typical-number-of-words-they-can-say-in-one-minute
# "publishers recommend books on tape to be voiced at 150-160 wpm"
podcast_words_per_minute = 125  # well below stated suggestion

podcast_default_minutes = 20

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
