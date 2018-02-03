from datetime import datetime

from pytest import mark

from app.twitter_learning_journal.models.video import Video


def test_video():
    id = 1
    screen_name = 'screen_name'
    title = 'title'
    classification = 'classification'
    duration = 5
    start_date = datetime.now()
    stop_date = datetime.now()

    expected_str = f'<Video(id={id}, ' \
                   f'screen_name={screen_name}, ' \
                   f'title={title}, ' \
                   f'classification={classification}, ' \
                   f'duration={duration}, ' \
                   f'start_date={start_date}, ' \
                   f'stop_date={stop_date})>'

    video = Video(
        id=1,
        screen_name=screen_name,
        title=title,
        classification=classification,
        duration=duration,
        start_date=start_date,
        stop_date=stop_date
    )

    assert expected_str == str(video)


@mark.parametrize("video_id, other_video_id, expected_result",
                  [
                      (None, None, False),
                      (1, None, False),
                      (None, 1, False),
                      (1, 1, True),
                      (1, 2, False),
                  ])
def test_video_equal(video_id, other_video_id, expected_result):
    assert expected_result == (Video(id=video_id) == Video(id=other_video_id))
