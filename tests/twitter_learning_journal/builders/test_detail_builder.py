from pytest import mark

from app.twitter_learning_journal.builders.detail_builder import DetailBuilder
from app.twitter_learning_journal.models.tweet import Tweet


def test_detail_builder_init():
    tweet = Tweet()

    detail_builder = DetailBuilder(tweet)

    assert tweet == detail_builder.tweet


@mark.parametrize('expected_title, tweet_text', [
    ('Title', 'Title'),
    ('title', 'title\n'),
    ('title', 'title\nextn'),
    ('url_value',)

])
def test_build_title():
    pass
