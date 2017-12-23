from datetime import datetime

from app.twitter_learning_journal.models.detail import Detail


def test_detail():
    start_date = datetime.now()
    stop_date = datetime.now()
    _type = 'type'
    title = 'title'
    classification = 'classification'

    expected_str = '<Detail(id=1, ' \
                   f'tweet_id=None, ' \
                   f'start_date={start_date}, ' \
                   f'stop_date={stop_date}, ' \
                   f'type={_type}, ' \
                   f'title={title}, ' \
                   f'classification={classification})>'

    detail = Detail(
        id=1,
        start_date=start_date,
        stop_date=stop_date,
        type=_type,
        title=title,
        classification=classification
    )

    assert None == detail.tweet
    assert expected_str == str(detail)
