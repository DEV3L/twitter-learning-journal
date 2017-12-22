from pytest import mark

from app.twitter_learning_journal.models.tweet import Tweet
from app.twitter_learning_journal.services.tweets_processing_service import TweetsProcessingService
from tests.twitter_learning_journal import test_classification_model


def test_tweets_processing_service_init():
    tweets = []
    tweets_processing_service = TweetsProcessingService(tweets)

    assert tweets == tweets_processing_service.tweets


def test_count_words_in_tweets():
    tweets = [
        Tweet(full_text='word'),
        Tweet(full_text='word\nword'),
        Tweet(full_text=' wor''d. , ! * ( ) = + ` ~ " '' word word'),
    ]

    tweets_processing_service = TweetsProcessingService(tweets)
    tweets_processing_service.count_tweet_words()

    assert 6 == sum([tweet.word_count for tweet in tweets])


@mark.parametrize("expected_classification_values, hashtags, full_texts",
                  [  # expected_classification_values, hashtags, full_text
                      ([''], [''], [None, ]),
                      (['tag'], ['tag'], [None]),
                      (['tag', ''], ['tag', 'tagz'], [None, None]),
                      (['tag', ''], ['tag', 'tagz'], [None, None]),
                      (['tag', 'tag'], ['tag|tags', 'tag'], [None, None]),
                      (['tag'], ['tag|not_tag'], [None]),
                      ([''], ['tagz'], [None]),
                      (['tag'], [''], ['tag']),
                      (['tag'], ['tag'], ['not tag']),
                      (['not_tag'], ['tag'], ['not_tag not_tag']),
                  ])
def test_classify_tweets(expected_classification_values, hashtags, full_texts):
    tweets = [Tweet(hashtags=hashtag, full_text=full_text)
              for hashtag, full_text in zip(hashtags, full_texts)]
    tweets_processing_service = TweetsProcessingService(tweets, classification_model=test_classification_model)

    tweets_processing_service.classify_tweets()

    for count, expected_classification_value in enumerate(expected_classification_values):
        assert expected_classification_value == tweets_processing_service.tweets[count].classification
