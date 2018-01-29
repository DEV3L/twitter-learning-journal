from sqlalchemy import Column, Integer, String, DateTime

from app.twitter_learning_journal.models import Base


class Book(Base):
    __tablename__ = 'book'

    id = Column(Integer, primary_key=True)

    screen_name = Column(String)
    title = Column(String)
    classification = Column(String)
    pages = Column(Integer)

    start_date = Column(DateTime)
    stop_date = Column(DateTime)

    def __str__(self):
        return f'<Book(id={self.id}, ' \
               f'screen_name={self.screen_name}, ' \
               f'title={self.title}, ' \
               f'classification={self.classification}, ' \
               f'pages={self.pages}, ' \
               f'start_date={self.start_date}, ' \
               f'stop_date={self.stop_date})>'

    def __eq__(self, other):
        return self.id is not None and other.id is not None and self.id == other.id
