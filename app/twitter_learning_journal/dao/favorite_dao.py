from sqlalchemy import exists

from app.twitter_learning_journal.database.sqlalchemy_database import Database
from app.twitter_learning_journal.models.favorite import Favorite


class FavoriteDao:
    def __init__(self, database: 'Database'):
        self._database = database

    def add(self, favorite: 'Favorite'):
        self._database.add(favorite)

    def add_all(self, favorites: list):
        self._database.add_all(favorites)

    def exists(self, id: int) -> bool:
        return self._database.query(exists().where(Favorite.id == id)).scalar()

    def by_id(self, id: int) -> 'Favorite':
        return self._database.query(Favorite).filter(Favorite.id == id).first()

    def query_all(self) -> list:
        return self._database.query(Favorite).all()
