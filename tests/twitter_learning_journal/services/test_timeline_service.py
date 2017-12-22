from collections import defaultdict

from app.twitter_learning_journal.services.timeline_service import TimelineService


def test_timeline_service_init():
    favorites = []
    timeline_service = TimelineService(favorites)

    assert defaultdict(dict) == timeline_service.timeline
    assert favorites == timeline_service.favorites
