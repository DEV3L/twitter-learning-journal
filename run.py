from app.twitter_learning_journal.dao.tweet_dao import TweetDao
from app.twitter_learning_journal.database.sqlalchemy_database import Database, build_tables
from app.twitter_learning_journal.retrievers.twitter.api import get_api
from app.twitter_learning_journal.retrievers.twitter_retriever import TwitterRetriever


def extract_from_twitter_feed(tweet_dao, screen_name):
    api = get_api()
    twitter_tweet_retriever = TwitterRetriever(api, tweet_dao, screen_name)
    twitter_tweet_retriever.fetch()
    twitter_favorite_retriever = TwitterRetriever(api, tweet_dao, screen_name, is_favorite=True)
    twitter_favorite_retriever.fetch()


if __name__ == '__main__':
    screen_name = 'dev3l_'

    database = Database()
    build_tables(database)

    tweet_dao = TweetDao(database)

    extract_from_twitter_feed(tweet_dao, screen_name)

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
