from datetime import datetime

from app.twitter_learning_journal.transformers.transform_datetime import transform_datetime_to_iso_date_str


def test_transform_datetime_to_iso_date_str():
    input_datetime = datetime(2017, 12, 19)

    assert '2017-12-19' == transform_datetime_to_iso_date_str(input_datetime)
