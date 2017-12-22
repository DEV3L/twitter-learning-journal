from unittest.mock import MagicMock, patch

from pytest import mark

from app.twitter_learning_journal.classifiers import global_classification_model
from app.twitter_learning_journal.classifiers.tweet_classifier import TweetClassifier, _extract_classification
from app.twitter_learning_journal.models.tweet import Tweet
from tests.twitter_learning_journal import test_classification_model


def test_tweet_classifier_init():
    tweet = Tweet()
    tweet_classifier = TweetClassifier(tweet)

    assert tweet == tweet_classifier.tweet
    assert global_classification_model == tweet_classifier.classification_model

    tweet_classifier = TweetClassifier(tweet, classification_model=test_classification_model)

    assert tweet == tweet_classifier.tweet
    assert test_classification_model == tweet_classifier.classification_model


@mark.parametrize('hashtags, full_text, expected_classification',
                  [
                      (None, None, ''),
                      ('', '', ''),
                      ('tag', '', 'tag'),
                      ('', 'tag', 'tag'),
                      ('tag', 'not_tag', 'tag'),
                      ('not_tag', 'tag', 'not_tag'),
                      ('tagz', 'tagz', ''),
                      ('tag', 'tag', 'tag'),
                  ])
def test_classify(hashtags, full_text, expected_classification):
    tweet = Tweet(hashtags=hashtags, full_text=full_text)
    tweet_classifier = TweetClassifier(tweet, classification_model=test_classification_model)
    tweet_classifier.classify()

    assert expected_classification == tweet.classification


@mark.parametrize('tag_count, not_tag_count, words, delimiter',
                  [
                      (0, 0, '', None),
                      (1, 0, 'tag', None),
                      (1, 0, 'tag tags', None),
                      (1, 1, 'tag not_tag', None),
                      (0, 0, 'tagz', None),
                  ])
def test_classify_words_(tag_count, not_tag_count, words, delimiter):
    expected_classification = {}

    if tag_count:
        expected_classification['tag'] = tag_count

    if not_tag_count:
        expected_classification['not_tag'] = not_tag_count

    tweet_classifier = TweetClassifier(Tweet(), classification_model=test_classification_model)
    classification = tweet_classifier._classify_words(words, delimiter=delimiter)
    assert expected_classification == classification


@patch('app.twitter_learning_journal.classifiers.tweet_classifier.TweetClassifier._classify_words')
def test_classify_hashtags(mock_classify_words):
    mock_tweet = MagicMock()
    tweet_classifier = TweetClassifier(mock_tweet, classification_model=test_classification_model)

    classified_hashtags = tweet_classifier._classify_hashtags()

    assert mock_classify_words.return_value == classified_hashtags
    mock_classify_words.assert_called_with(mock_tweet.hashtags, delimiter='|')


@patch('app.twitter_learning_journal.classifiers.tweet_classifier.TweetClassifier._classify_words')
def test_classify_full_text(mock_classify_words):
    mock_tweet = MagicMock()
    tweet_classifier = TweetClassifier(mock_tweet, classification_model=test_classification_model)

    classified_full_text = tweet_classifier._classify_full_text()

    assert mock_classify_words.return_value == classified_full_text
    mock_classify_words.assert_called_with(mock_tweet.full_text)


@mark.parametrize('classification, expected_value',
                  [
                      ({}, ''),
                      ({'a': 1, 'b': 2}, 'b'),
                      ({'a': 2, 'b': 2}, 'a'),
                  ])
def test_extract_classification(classification, expected_value):
    assert expected_value == _extract_classification(classification)
