from unittest.mock import patch

from app.twitter_learning_journal.classifiers.tweets_classifier import TweetsClassifier


def test_tweets_classifier_init():
    tweets_classifier = TweetsClassifier([])
    assert [] == tweets_classifier.tweets


@patch('app.twitter_learning_journal.classifiers.tweets_classifier.TweetsProcessingService')
def test_classify(mock_tweets_processing_service):
    mock_tweets_processing_service_instance = mock_tweets_processing_service.return_value
    tweets_classifier = TweetsClassifier([])

    tweets_classifier.classify()

    mock_tweets_processing_service.assert_called_with(tweets_classifier.tweets)
    assert mock_tweets_processing_service_instance.count_tweet_words.called
    assert mock_tweets_processing_service_instance.classify_tweets.called
    assert mock_tweets_processing_service_instance.sub_classify_unclassified_tweets.called
