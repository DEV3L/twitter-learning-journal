from app.twitter_learning_journal.extractors.tweet.video_extractor import VideoExtractor
from app.twitter_learning_journal.models.tweet import Tweet


def test_init():
    tweet = Tweet()
    video_extractor = VideoExtractor(tweet)

    assert tweet == video_extractor.tweet
