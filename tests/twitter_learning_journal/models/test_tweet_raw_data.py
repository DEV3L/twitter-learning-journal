from app.twitter_learning_journal.models.tweet import Tweet
from app.twitter_learning_journal.models.tweet_raw_data import TweetRawData


def test_raw_data_init():
    # class RawData(Base):
    #     __tablename__ = 'raw_data'
    #
    #     id = Column(Integer, primary_key=True)
    #
    #     tweet_id = Column(Integer, ForeignKey('tweet.id'))
    #     tweet = relationship('Tweet', back_populates='raw_data')
    #
    #     raw_data = Column(Binary, default=None)
    tweet_raw_data = TweetRawData(id=1,
                                  tweet_id=2,
                                  tweet=Tweet(id=2),
                                  raw_data=b'raw_data')
    # _type = 'type'
    # title = 'title'
    # url = 'url'
    # count = 0
    # classification = 'classification'
    # is_fully_classified = None
    #
    # expected_str = '<Detail(id=1, ' \
    #                f'tweet_id=None, ' \
    #                f'type={_type}, ' \
    #                f'title={title}, ' \
    #                f'url={url}, ' \
    #                f'count={count}, ' \
    #                f'classification={classification}, ' \
    #                f'is_fully_classified={is_fully_classified})>'
    #
    # detail = Detail(
    #     id=1,
    #     type=_type,
    #     title=title,
    #     url=url,
    #     count=count,
    #     classification=classification
    # )
