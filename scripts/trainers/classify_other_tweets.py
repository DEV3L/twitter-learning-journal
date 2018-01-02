from app.twitter_learning_journal.dao.tweet_dao import TweetDao
from app.twitter_learning_journal.database.sqlalchemy_database import Database
from app.twitter_learning_journal.models.detail import Detail


def classify_other_details():
    database = Database()
    tweet_dao = TweetDao(database)
    details = tweet_dao._database.query(Detail).all()
    details = [detail for detail in details if detail.type == 'other']

    for detail in details:
        print(detail)
