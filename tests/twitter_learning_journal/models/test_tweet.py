from datetime import datetime

from app.twitter_learning_journal.models.tweet import Tweet


def test_str():
    _now = datetime.now()
    tweet = Tweet(
        id=1,
        created_at=_now,
        full_text='full_text',
        hashtags='hashtags',
        type='favorite',
        word_count=0,
        classification='classification'
    )

    assert '<Tweet(id=1, ' \
           f'created_at={_now}, ' \
           'full_text=full_text, ' \
           'type=favorite, ' \
           'hashtags=hashtags, ' \
           'word_count=0, ' \
           'classification=classification)>' == str(tweet)
