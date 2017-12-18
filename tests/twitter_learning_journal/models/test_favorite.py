from datetime import datetime

from app.twitter_learning_journal.models.favorite import Favorite


def test_str():
    _now = datetime.now()
    favorite = Favorite(
        id=1,
        created_at=_now,
        full_text='full_text',
        hashtags='hashtags'
    )

    assert f'<Favorite(id=1, created_at={_now}, full_text=full_text, hashtags=hashtags)>' == str(favorite)
