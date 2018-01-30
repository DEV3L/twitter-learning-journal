from app.twitter_learning_journal.models.detail import Detail
from app.twitter_learning_journal.models.tweet import Tweet


class DetailBuilder:
    default_detail_type = 'blog'
    default_detail_size = 500
    max_title_length = 30

    def __init__(self, tweet: Tweet, detail_type=None):
        self.tweet = tweet
        self.detail_type = detail_type or self.default_detail_type

    def build(self):
        detail = Detail(title=self.title,
                        tweet_id=self.tweet.id,
                        url=self.tweet.urls,
                        type=self.detail_type,
                        is_fully_classified=False,
                        classification=self.tweet.classification,
                        count=self.default_detail_size)
        return detail

    @property
    def title(self):
        title = ''
        full_text = self.tweet.full_text

        if not full_text.strip():
            return title

        line_number = 0

        while not title:
            title = self.tweet.full_text.splitlines()[line_number]
            line_number += 1

        if len(title) > self.max_title_length:
            title = title[:self.max_title_length]

        return title
