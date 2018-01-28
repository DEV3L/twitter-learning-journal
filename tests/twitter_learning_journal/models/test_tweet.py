from datetime import datetime

from app.twitter_learning_journal.models.tweet import Tweet


def test_tweet():
    screen_name = 'screen_name'
    created_at = datetime.now()
    full_text = 'full_text'
    _type = 'type'
    hashtags = 'hashtags'
    urls = None
    count = 0
    classification = 'classification'

    expected_raw_data = b'raw_data'
    expected_str = '<Tweet(id=1, ' \
                   f'screen_name={screen_name}, ' \
                   f'created_at={created_at}, ' \
                   f'full_text={full_text}, ' \
                   f'type={_type}, ' \
                   f'hashtags={hashtags}, ' \
                   f'urls={urls}, ' \
                   f'count={count}, ' \
                   f'classification={classification})>'

    tweet = Tweet(
        screen_name=screen_name,
        id=1,
        created_at=created_at,
        full_text=full_text,
        hashtags=hashtags,
        type=_type,
        count=count,
        classification=classification
    )

    assert [] == tweet.details
    assert 0 == tweet.count
    assert None == tweet.is_fully_classified
    assert expected_str == str(tweet)
