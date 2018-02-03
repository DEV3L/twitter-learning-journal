from app.twitter_learning_journal.models.tweet import Tweet


class VideoExtractor:
    def __init__(self, tweet: Tweet):
        self.tweet = tweet
