import logging

from app.twitter_learning_journal.builders.detail_builder import build_detail
from app.twitter_learning_journal.dao.tweet_dao import TweetDao
from app.twitter_learning_journal.transformers.transform_str import remove_ignore_characters_from_str
from scripts.trainers.script_dependencies import make_database

logging_level = logging.WARNING
logger = logging.getLogger('detail_trainer')


def _log(message):
    logger.log(logging_level, message)

def train_details():
    database = make_database()
    tweet_dao = TweetDao(database)

    _log('Detail trainer: Iterate through all non fully classified Tweets')
    _tweets = tweet_dao.query_all()

    _log(f'Total Tweets: {len(_tweets)}')

    _tweets = get_unclassified_tweets(_tweets)

    total = len(_tweets)

    _log(f'Total Tweets Not Fully Classified: {total}')

    keywords = ['read',
                'listen',
                'listened',
                'listened to',
                'watched',
                'watch',
                'attended',
                'attending']

    total_processed = 0
    total_details = 0

    for tweet in _tweets:
        has_keywords = False
        has_quoted_keywords = False
        _full_text = ' '.join(remove_ignore_characters_from_str(tweet.full_text).split()).lower()

        _log('-----TWEET-----')
        _log(f' classification: {tweet.classification}')
        _log(f' url: {tweet.urls}')
        _log(f' {tweet.full_text}')

        for keyword in keywords:
            if keyword in _full_text:
                logger.warning(f'"{keyword}" found in {_full_text}')
                has_keywords = True

            if f'"{keyword}"' in _full_text or f"'{keyword}'" in _full_text:
                has_quoted_keywords = True

        if has_keywords and not has_quoted_keywords:
            # handle these later books, audio, videos
            create_detail(tweet, database, detail_type='keyword')
        elif not tweet.urls:
            _log('No details for tweet')
            _log('processed')
            tweet.is_fully_classified = True
        else:
            detail = create_detail(tweet, database)
            _log(f'Detail created: {detail}')

            total_details += 1

            tweet.is_fully_classified = True

        database.commit()
        total_processed += 1

    _log(total_processed)

    database.commit()
    _log('Done')


def create_detail(tweet, database, *, detail_type='blog'):
    detail = build_detail(tweet, detail_type=detail_type)
    _log(f'created:\n{detail}')
    database.add(detail)
    return detail


def get_unclassified_tweets(tweets):
    tweets = [tweet for tweet in tweets if not tweet.is_fully_classified]
    tweets = [tweet for tweet in tweets if tweet.type == 'tweet']
    tweets = sorted(tweets, key=lambda x: x.created_at, reverse=True)
    return tweets


if __name__ == '__main__':
    train_details()
