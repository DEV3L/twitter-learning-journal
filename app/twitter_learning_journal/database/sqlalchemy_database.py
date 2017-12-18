from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


class Database():
    def __init__(self):
        self._engine = create_engine('sqlite:///data/twitter-learning-journal', echo=True)

        Session = sessionmaker(bind=self._engine)
        self._session = Session()

    def add(self, entity):
        return self._session.add(entity)

    def query(self, entity):
        return self._session.query(entity)

    def commit(self):
        self._session.commit()
