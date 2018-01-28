from app.twitter_learning_journal.builders.detail_builder import DetailBuilder
from app.twitter_learning_journal.models.tweet import Tweet


def test_detail_builder_init():
    tweet = Tweet()

    detail_builder = DetailBuilder(tweet)

    assert tweet == detail_builder.tweet
