from app.twitter_learning_journal.database.sqlalchemy_database import Database
from app.twitter_learning_journal.models.detail import Detail
from app.twitter_learning_journal.retrievers.details.podcast import PodcastExtractor
from scripts.blogs import classify_blogs
from scripts.trainers.detail_trainer import train_details

if __name__ == '__main__':
    screen_name = 'jrj2280'

    database = Database()
    # build_tables(database)
    # tweet_dao = TweetDao(database)
    #
    # twitter_tweet_retriever = TwitterRetriever(tweet_dao, screen_name)
    # twitter_tweet_retriever.fetch()
    #
    # tweets = tweet_dao.query_all()
    # tweets_classifier = TweetsClassifier(tweets)
    # tweets_classifier.classify()
    # database.commit_entities(tweets)

    train_details(database)

    details = database.query(Detail).all()

    classified_blogs, unclassified_blogs = classify_blogs(details)
    database.add_all(classified_blogs)
    database.add_all(unclassified_blogs)
    database.commit()

    podcast_extractor = PodcastExtractor(details)
    podcast_extractor.classify()

    database.add_all(podcast_extractor.details)
    database.commit()
