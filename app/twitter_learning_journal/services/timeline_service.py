from collections import defaultdict


class TimelineService:
    def __init__(self, favorites: list):
        self.timeline = defaultdict(dict)
        self.favorites = favorites
