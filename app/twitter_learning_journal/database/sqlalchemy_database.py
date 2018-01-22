from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.twitter_learning_journal.models import Base


class Database():
    def __init__(self, database_url='data/twitter-learning-journal', *, echo=True):
        self._engine = create_engine(f'sqlite:///{database_url}', echo=echo)

        Session = sessionmaker(bind=self._engine)
        self._session = Session()

    def query(self, entity):
        return self._session.query(entity)

    def add(self, entity):
        self._session.add(entity)

    def add_all(self, entities: list):
        self._session.add_all(entities)

    def commit(self):
        self._session.commit()

    def commit_entities(self, entities: list):
        self.add_all(entities)
        self.commit()

def build_tables(database):
    Base.metadata.create_all(database._engine)
