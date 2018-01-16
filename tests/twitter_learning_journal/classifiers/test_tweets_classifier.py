from unittest.mock import MagicMock, patch

from app.twitter_learning_journal.classifiers.tweets_classifier import TweetsClassifier


def test_tweets_classifier_init():
    tweets_classifier = TweetsClassifier([], None)
    assert [] == tweets_classifier.tweets
    assert None == tweets_classifier.tweet_dao


def test_save_tweet():
    mock_tweet_dao = MagicMock()
    tweets_classifier = TweetsClassifier([], mock_tweet_dao)

    tweets = ['list']
    tweets_classifier._save_tweets(tweets)

    mock_tweet_dao.add_all.assert_called_with(tweets)
    assert mock_tweet_dao.commit.called


@patch('app.twitter_learning_journal.classifiers.tweets_classifier.TweetsProcessingService')
def test_classify(mock_tweets_processing_service):
    mock_tweets_processing_service_instance = mock_tweets_processing_service.return_value
    mock_save_tweets = MagicMock()
    tweets_classifier = TweetsClassifier([], None)
    tweets_classifier._save_tweets = mock_save_tweets

    tweets_classifier.classify()

    mock_tweets_processing_service.assert_called_with(tweets_classifier.tweets)
    assert mock_tweets_processing_service_instance.count_tweet_words.called
    assert mock_tweets_processing_service_instance.classify_tweets.called
    mock_save_tweets.assert_called_with(mock_tweets_processing_service.return_value.tweets)
