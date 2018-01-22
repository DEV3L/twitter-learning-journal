from pytest import mark

from app.twitter_learning_journal.models.tweet import Tweet
from app.twitter_learning_journal.services.tweets_processing_service import TweetsProcessingService, \
    add_words_to_classification_model
from tests.twitter_learning_journal import test_classification_model


def test_tweets_processing_service_init():
    expected_weight_text = 1.0
    expected_sub_weight_text = .1
    expected_weight_hashtag = 3.0
    expected_sub_weight_hashtag = .3

    tweets = []
    tweets_processing_service = TweetsProcessingService(tweets)

    assert expected_weight_text == tweets_processing_service.weight_text
    assert expected_sub_weight_text == tweets_processing_service.sub_weight_text
    assert expected_weight_hashtag == tweets_processing_service.weight_hashtag
    assert expected_sub_weight_hashtag == tweets_processing_service.sub_weight_hashtag
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
                  [
                      ([''], [''], [None, ]),
                      (['tag'], ['tag'], [None]),
                      (['tag', ''], ['tag', 'tagz'], [None, None]),
                      (['tag', ''], ['tag', 'tagz'], [None, None]),
                      (['tag', 'tag'], ['tag|tags', 'tag'], [None, None]),
                      (['tag'], ['tag|not_tag'], [None]),
                      ([''], ['tagz'], [None]),
                      (['tag'], [''], ['tag']),
                      (['tag'], ['tag'], ['not tag']),
                      (['tag'], ['tag'], ['not_tag not_tag']),  # weight of hashtag > word
                  ])
def test_classify_tweets(expected_classification_values, hashtags, full_texts):
    tweets = [Tweet(hashtags=hashtag, full_text=full_text)
              for hashtag, full_text in zip(hashtags, full_texts)]
    tweets_processing_service = TweetsProcessingService(tweets, classification_model=test_classification_model)

    tweets_processing_service.classify_tweets()

    for count, expected_classification_value in enumerate(expected_classification_values):
        assert expected_classification_value == tweets_processing_service.tweets[count].classification


def test_build_sub_classification_model():
    classification = 'classification'

    expected_classification_model = {
        classification: {'full', 'text', 'words', 'swords'}
    }

    tweets = [
        Tweet(hashtags='hashtag', full_text='full text words', classification=classification),
        Tweet(hashtags='hashtag', full_text='full swords', classification=classification)]

    classification_model = {classification: set()}
    tweets_processing_service = TweetsProcessingService(tweets, classification_model=classification_model)
    sub_classification_model = tweets_processing_service._build_sub_classification_model()

    assert classification_model != sub_classification_model
    assert expected_classification_model == sub_classification_model


# move to separate test file when add_words_to_classification_model extracted from file
def test_add_words_to_classification_model():
    classification = 'classification'
    full_text = 'full text"Words'

    expected_classification_model = {
        classification: {'full', 'text', 'words'}
    }

    classification_model = {classification: set()}
    tweet = Tweet(full_text=full_text, classification=classification)

    add_words_to_classification_model(classification_model, tweet)

    assert expected_classification_model == classification_model
