#!/usr/bin/env python
# encoding: utf-8

"""
This is my 'hacker-mode' file!

It has been stitched together from a few github gist files
"""

# https://gist.github.com/yanofsky/5436496
# https://gist.github.com/datagrok/74a71f572493e603919e
from collections import defaultdict
from datetime import datetime, timedelta

from app.twitter_learning_journal.classifiers import global_classification_model, get_classification_model
from app.twitter_learning_journal.dao.tweet_dao import TweetDao
from app.twitter_learning_journal.models.detail import Detail
from app.twitter_learning_journal.services.tweets_processing_service import TweetsProcessingService
from app.twitter_learning_journal.transformers.transform_datetime import transform_datetime_to_iso_date_str
from app.twitter_learning_journal.transformers.transform_str import remove_ignore_characters_from_str
from app.twitter_learning_journal.twitter_api.tweets import Tweets


def collect(api, screen_name, *, tweet_type='favorite'):
    tweets = Tweets(api, screen_name, tweet_type=tweet_type)
    return tweets.get()


def save_tweets(tweet_dao, tweets):
    for tweet in tweets:
        if not tweet_dao.exists(tweet.id):
            tweet_dao.add(tweet)

    tweet_dao.commit()


def classify_tweets(tweet_dao):
    tweets = tweet_dao.query_all()

    tweets_processing_service = TweetsProcessingService(tweets)
    tweets_processing_service.count_tweet_words()
    tweets_processing_service.classify_tweets()

    tweet_dao.add_all(tweets_processing_service.tweets)
    tweet_dao.commit()


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

def timeline(tweet_dao: TweetDao, details: list, audio_details: list, books: list):
    # from here below still needs to be gracefully implemented

    tweets = tweet_dao.query_all()
    _details = tweet_dao._database.query(Detail).all()

    _timeline = defaultdict(list)

    min_date = datetime(year=2017, month=11, day=28)
    max_date = datetime(year=2017, month=12, day=28, hour=23, minute=59)

    _tweets = [tweet for tweet in tweets if tweet.created_at >= min_date and tweet.created_at <= max_date]
    tweet_count = len(_tweets)

    start_date = datetime(year=2017, month=11, day=28)

    while start_date < max_date:
        _timeline[transform_datetime_to_iso_date_str(start_date)] = []
        start_date += timedelta(days=1)

    twitter_words = 0

    for tweet in tweets:
        twitter_words += tweet.word_count
        _timeline[transform_datetime_to_iso_date_str(tweet.created_at)].append(tweet)

    per_day_count_by_classification = []
    for key in sorted(global_classification_model.keys()):
        per_day_count_by_classification.append({key: []})

    return tweets
