#!/usr/bin/env python
# encoding: utf-8

"""
This is my 'hacker-mode' file!

It has been stitched together from a few github gist files
"""

# https://gist.github.com/yanofsky/5436496
# https://gist.github.com/datagrok/74a71f572493e603919e

from app.twitter_learning_journal.classifiers import get_classification_model
from app.twitter_learning_journal.services.tweets_processing_service import TweetsProcessingService
from app.twitter_learning_journal.transformers.transform_str import remove_ignore_characters_from_str


def add_sub_classification_to_models(tweet_dao):
    tweets = tweet_dao.query_all()

    unclassified_tweets = [tweet for tweet in tweets if not tweet.classification]
    classified_tweets = [tweet for tweet in tweets if tweet.classification]

    sub_classification_model = dict(get_classification_model(None))

    for tweet in classified_tweets:
        cleaned_full_text = remove_ignore_characters_from_str(tweet.full_text)
        updated_classification = sub_classification_model[tweet.classification].union(cleaned_full_text)
        sub_classification_model[tweet.classification] = updated_classification

    tweets_processing_service = TweetsProcessingService(unclassified_tweets,
                                                        classification_model=sub_classification_model,
                                                        weight_text=.1, weight_hashtag=.5)
    tweets_processing_service.classify_tweets()

    tweet_dao.add_all(tweets_processing_service.tweets)
    tweet_dao.commit()
