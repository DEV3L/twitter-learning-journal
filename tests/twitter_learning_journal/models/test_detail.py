from pytest import mark

from app.twitter_learning_journal.models.detail import Detail


def test_detail():
    _type = 'type'
    title = 'title'
    url = 'url'
    count = 0
    classification = 'classification'
    is_fully_classified = None

    expected_str = '<Detail(id=1, ' \
                   f'tweet_id=None, ' \
                   f'type={_type}, ' \
                   f'title={title}, ' \
                   f'url={url}, ' \
                   f'count={count}, ' \
                   f'classification={classification}, ' \
                   f'is_fully_classified={is_fully_classified})>'

    detail = Detail(
        id=1,
        type=_type,
        title=title,
        url=url,
        count=count,
        classification=classification
    )

    assert None == detail.tweet
    assert expected_str == str(detail)


@mark.parametrize("detail_id, other_detail_id, expected_result",
                  [
                      (None, None, False),
                      (1, None, False),
                      (None, 1, False),
                      (1, 1, True),
                      (1, 2, False),
                  ])
def test_detail_equal(detail_id, other_detail_id, expected_result):
    assert expected_result == (Detail(id=detail_id) == Detail(id=other_detail_id))
