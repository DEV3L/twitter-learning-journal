from pytest import mark

from app.twitter_learning_journal.builders.detail_builder import DetailBuilder
from app.twitter_learning_journal.models.tweet import Tweet


def test_detail_builder_init():
    tweet = Tweet()

    detail_builder = DetailBuilder(tweet)

    assert tweet == detail_builder.tweet
    assert 'blog' == detail_builder.default_detail_type


def test_build_details():
    expected_title = 'full_text'
    expected_type = 'blog'

    tweet = Tweet(
        id=1,
        full_text=f'{expected_title}\ntest',
        urls='urls',
        classification='classification'
    )
    detail_builder = DetailBuilder(tweet)

    detail = detail_builder.build()

    assert expected_title == detail.title
    assert tweet.id == detail.tweet_id
    assert tweet.urls == detail.url
    assert expected_type == detail.type
    assert not detail.is_fully_classified
    assert tweet.classification == detail.classification
    assert detail_builder.default_detail_size == detail.count


@mark.parametrize('expected_title, full_text', [
    ('hello', 'hello\nsometest'),
    ('sometest', '\nsometest'),
    ('', ''),
    ('123456789112345678921234567893', '123456789112345678921234567893XXX'),
    ('candace', '\n\n\ncandace\nsome text'),
])
def test_title(expected_title, full_text):
    tweet = Tweet(full_text=full_text)
    detail_builder = DetailBuilder(tweet)

    assert expected_title == detail_builder.title
