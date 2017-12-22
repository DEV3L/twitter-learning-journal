from collections import defaultdict


class TimelineService:
    def __init__(self, tweets: list):
        self.timeline = defaultdict(dict)
        self.tweets = tweets
