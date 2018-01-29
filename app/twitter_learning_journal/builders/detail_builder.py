from app.twitter_learning_journal.models.detail import Detail
from app.twitter_learning_journal.models.tweet import Tweet
from app.twitter_learning_journal.transformers.transform_str import remove_ignore_characters_from_str

default_podcast_size = 20
default_video_size = 10
default_blog_size = 500


class DetailBuilder:
    def __init__(self, tweet: Tweet):
        self.tweet = tweet


def build_detail(tweet, *, detail_type='blog'):
    title = _build_title(tweet)

    detail = Detail(title=title,
                    tweet_id=tweet.id,
                    url=tweet.urls,
                    is_fully_classified=True,
                    classification=tweet.classification)

    _set_detail_type_and_size(detail, tweet)

    if detail_type:
        detail.type = detail_type

    return detail


def _build_title(tweet):
    _title = tweet.full_text.splitlines()[0]
    title = _title

    full_text_without_ignore_characters = remove_ignore_characters_from_str(tweet.full_text.lower())

    if tweet.urls and full_text_without_ignore_characters.startswith('listened to'):
        lines = full_text_without_ignore_characters.splitlines()
        title = ' '.join(lines[0].replace('listened to', '').split()).strip()

    return title


def _set_detail_type_and_size(detail, tweet):
    if 'listened to' in tweet.full_text.lower():
        detail.type = 'podcast'
        detail.count = 20
    else:
        detail.type = 'blog'

        detail.count = default_blog_size
