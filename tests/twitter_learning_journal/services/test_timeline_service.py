from collections import defaultdict

from app.twitter_learning_journal.services.timeline_service import TimelineService


def test_timeline_service_init():
    tweets = []
    timeline_service = TimelineService(tweets)

    assert defaultdict(dict) == timeline_service.timeline
    assert tweets == timeline_service.tweets
