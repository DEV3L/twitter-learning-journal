from sqlalchemy import Binary
from sqlalchemy import Column, ForeignKey, Integer
from sqlalchemy.orm import relationship

from app.twitter_learning_journal.models import Base


class RawData(Base):
    __tablename__ = 'raw_data'

    id = Column(Integer, primary_key=True)

    tweet_id = Column(Integer, ForeignKey('tweet.id'))
    tweet = relationship('Tweet', back_populates='raw_data')

    raw_data = Column(Binary, default=None)
