from app.twitter_learning_journal.classifiers.tweets_classifier import TweetsClassifier
from app.twitter_learning_journal.dao.tweet_dao import TweetDao
from app.twitter_learning_journal.database.sqlalchemy_database import Database, build_tables
from app.twitter_learning_journal.retrievers.twitter_retriever import TwitterRetriever

if __name__ == '__main__':
    screen_name = 'dev3l_'

    database = Database()
    build_tables(database)
    tweet_dao = TweetDao(database)

    twitter_tweet_retriever = TwitterRetriever(tweet_dao, screen_name)
    twitter_tweet_retriever.fetch()

    tweets = tweet_dao.query_all()
    tweets_classifier = TweetsClassifier(tweets)
    tweets_classifier.classify()
    database.commit_entities(tweets)

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
