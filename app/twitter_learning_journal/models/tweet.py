from sqlalchemy import Column, Integer, String, DateTime

from app.twitter_learning_journal.models import Base


class Tweet(Base):
    __tablename__ = 'tweet'

    id = Column(Integer, primary_key=True)
    created_at = Column(DateTime)
    full_text = Column(String)
    hashtags = Column(String)
    type = Column(String)
    word_count = Column(Integer, default=0)
    classification = Column(String)

    def __str__(self):
        return f'<Tweet(id={self.id}, ' \
               f'created_at={self.created_at}, ' \
               f'full_text={self.full_text}, ' \
               f'type={self.type}, ' \
               f'hashtags={self.hashtags}, ' \
               f'word_count={self.word_count}, ' \
               f'classification={self.classification})>'

    def __eq__(self, other):
        equal = self.id == other.id \
                and self.created_at == other.created_at \
                and self.full_text == other.full_text \
                and self.hashtags == other.hashtags

        return equal
