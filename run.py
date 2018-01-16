from app.twitter_learning_journal.dao.tweet_dao import TweetDao
from app.twitter_learning_journal.database.sqlalchemy_database import Database, build_tables
from app.twitter_learning_journal.retrievers.twitter.api import get_api
from tweet_dumper import collect

if __name__ == '__main__':
    screen_name = 'dev3l_'

    database = Database()
    tweet_dao = TweetDao(database)

    build_tables(database)

    # extract
    api = get_api()
    tweets = collect(api, screen_name, tweet_type='tweet')
    favorites = collect(api, screen_name)
    #
    # save_tweets(tweet_dao, favorites)
    # save_tweets(tweet_dao, tweets)
    #
    # # transform
    # classify_tweets(tweet_dao)
    #
    # add_sub_classification_to_models(tweet_dao)
    #
    # train_details()
    #
    # count_html_words()
    #
    # details = database.query(Detail).all()
    # podcast_details = count_podcast_words(details)
    # database.add_all(podcast_details)
    # database.commit()
    #
    # classify_keyword_tweets()
    # classify_other_details()
