from sqlalchemy import exists

from app.twitter_learning_journal.database.sqlalchemy_database import Database
from app.twitter_learning_journal.models.tweet import Tweet


class TweetDao:
    def __init__(self, database: 'Database'):
        self._database = database

    def add(self, tweet: 'Tweet'):
        self._database.add(tweet)

    def add_all(self, tweets: list):
        self._database.add_all(tweets)

    def exists(self, id: int) -> bool:
        return self._database.query(exists().where(Tweet.id == id)).scalar()

    def by_id(self, id: int) -> 'Tweet':
        return self._database.query(Tweet).filter(Tweet.id == id).first()

    def query_all(self) -> list:
        return self._database.query(Tweet).all()
