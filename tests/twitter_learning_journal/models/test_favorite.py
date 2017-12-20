from datetime import datetime

from app.twitter_learning_journal.models.favorite import Favorite


def test_str():
    _now = datetime.now()
    favorite = Favorite(
        id=1,
        created_at=_now,
        full_text='full_text',
        hashtags='hashtags',
        word_count=0,
        classification='classification'
    )

    assert f'<Favorite(id=1, ' \
           f'created_at={_now}, ' \
           f'full_text=full_text, ' \
           f'hashtags=hashtags, ' \
           f'word_count=0, ' \
           f'classification=classification)>' == str(favorite)
