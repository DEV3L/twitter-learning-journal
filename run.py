from app.twitter_learning_journal.dao.tweet_dao import TweetDao
from app.twitter_learning_journal.database.sqlalchemy_database import Database
from app.twitter_learning_journal.twitter_api.api import get_api
from tweet_dumper import timeline, collect, save_tweets, build_tables, classify_tweets, classify_audible_books, \
    add_sub_classification_to_models

if __name__ == '__main__':
    screen_name = 'dev3l_'

    api = get_api()

    database = Database()
    tweet_dao = TweetDao(database)

    build_tables(database)

    favorites = collect(api, screen_name)
    tweets = collect(api, screen_name, tweet_type='tweet')

    save_tweets(tweet_dao, favorites)
    save_tweets(tweet_dao, tweets)

    classify_tweets(tweet_dao)

    add_sub_classification_to_models(tweet_dao)

    books = classify_audible_books()

    timeline(tweet_dao, books)
