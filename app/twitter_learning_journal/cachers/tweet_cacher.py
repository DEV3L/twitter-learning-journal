from app.twitter_learning_journal.cachers.cacher import Cacher
from app.twitter_learning_journal.models.tweet import Tweet


class TweetCacher(Cacher):
    def __init__(self, screen_name: str, tweet: Tweet):
        super().__init__(screen_name, tweet, tweet.id)
        self.tweet = tweet
