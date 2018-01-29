from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from app.twitter_learning_journal.models import Base


class Detail(Base):
    __tablename__ = 'detail'

    id = Column(Integer, primary_key=True)

    tweet_id = Column(Integer, ForeignKey('tweet.id'))
    tweet = relationship('Tweet', back_populates='details')

    type = Column(String)
    title = Column(String)
    url = Column(String)
    count = Column(Integer)
    classification = Column(String)
    is_fully_classified = Column(Boolean, default=False)

    def __str__(self):
        return f'<Detail(id={self.id}, ' \
               f'tweet_id={self.tweet_id}, ' \
               f'type={self.type}, ' \
               f'title={self.title}, ' \
               f'url={self.url}, ' \
               f'count={self.count}, ' \
               f'classification={self.classification}, ' \
               f'is_fully_classified={self.is_fully_classified})>'

    def __eq__(self, other):
        return self.id is not None and other.id is not None and self.id == other.id
