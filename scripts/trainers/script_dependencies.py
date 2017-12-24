from app.twitter_learning_journal.database.sqlalchemy_database import Database


def make_database():
    return Database(database_url='/Users/justinbeall/GITHUB/twitter-learning-journal/data/twitter-learning-journal')
