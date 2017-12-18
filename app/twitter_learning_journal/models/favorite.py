from sqlalchemy import Column, Integer, String, DateTime

from app.twitter_learning_journal.models import Base


class Favorite(Base):
    __tablename__ = 'favorite'

    id = Column(Integer, primary_key=True)
    created_at = Column(DateTime)
    full_text = Column(String)
    hashtags = Column(String)

    def __str__(self):
        return f'<Favorite(id={self.id}, created_at={self.created_at}, full_text={self.full_text}, hashtags={self.hashtags})>'

    def __eq__(self, other):
        equal = self.id == other.id
        equal = equal and self.created_at == other.created_at
        equal = equal and self.full_text == other.full_text
        equal = equal and self.hashtags == other.hashtags

        return equal
