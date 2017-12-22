#!/usr/bin/env python
# encoding: utf-8

"""
This is my 'hacker-mode' file!

It has been stitched together from a few github gist files
"""

# https://gist.github.com/yanofsky/5436496
# https://gist.github.com/datagrok/74a71f572493e603919e
from collections import defaultdict

from app.twitter_learning_journal.classifiers import global_classification_model
from app.twitter_learning_journal.dao.favorite_dao import FavoriteDao
from app.twitter_learning_journal.database.sqlalchemy_database import Database
from app.twitter_learning_journal.models import Base
from app.twitter_learning_journal.services.favorites_processing_service import FavoritesProcessingService
from app.twitter_learning_journal.transformers.transform_datetime import transform_datetime_to_iso_date_str
from app.twitter_learning_journal.twitter_api.api import get_api
from app.twitter_learning_journal.twitter_api.favorites import Favorites


def collect_favorites(screen_name):
    api = get_api()
    favorites = Favorites(api, screen_name)
    return favorites.get()


def write_favorites(favorites):
    database = Database()
    favorite_dao = FavoriteDao(database)

    for favorite in favorites:
        if not favorite_dao.exists(favorite.id):
            favorite_dao.add(favorite)

    database.commit()


def classify_favorites():
    database = Database()
    Base.metadata.create_all(database._engine)

    favorite_dao = FavoriteDao(database)
    favorites = favorite_dao.query_all()

    favorites_processing_service = FavoritesProcessingService(favorites)
    favorites_processing_service.count_words_in_favorites()
    favorites_processing_service.classify_favorites()

    favorite_dao.add_all(favorites_processing_service.favorites)
    database.commit()


def timeline():
    # from here below still needs to be gracefully implemented
    database = Database()
    Base.metadata.create_all(database._engine)

    favorite_dao = FavoriteDao(database)
    favorites = favorite_dao.query_all()

    _timeline = defaultdict(list)

    for favorite in favorites:
        _timeline[transform_datetime_to_iso_date_str(favorite.created_at)].append(favorite)

    per_day_count_by_classification = []
    for key in sorted(global_classification_model.keys()):
        per_day_count_by_classification.append({key: []})

    for key in sorted(_timeline.keys()):
        favorites = [favorite for favorite in _timeline[key]]

        word_count = sum([favorite.word_count for favorite in favorites])
        count = len(_timeline[key])

        classification_values = defaultdict(int)

        for favorite in favorites:
            classification_value = favorite.classification

            if not classification_value:
                classification_value = 'not_classified'

            classification_values[classification_value] += favorite.word_count

        display_str = ''
        for _key, value in classification_values.items():
            if display_str:
                display_str += ','

            display_str += f'{_key}={value}'

        for classification in per_day_count_by_classification:
            classification_name = next(iter(classification.keys()))
            classification_count = classification_values.get(classification_name)
            classification[classification_name].append(classification_count or 0)
            print()

        print(f'date={key}:favorites_count={count}:total_words={word_count}|classifications:{display_str}')

    print('---------- html categories ----------')
    print('[')
    for key in sorted(_timeline.keys()):
        print(f"'{key}',")
    print(']')

    print('--------------------')
    print('--------------------')
    print('--------------------')
    print('--------------------')
    print('--------------------')

    """
    series = [
        {
            name: 'John',
            data: [5, 3, 4, 7, 2, 2, 0, 5, 3, 4, 7, 2, 2, 0, 5, 3, 4, 7, 2, 2, 0, 5, 3, 4, 7, 2, 2, 0,
                5, 3, 4, 7, 2, 2, 0, 5, 3, 4, 7, 2, 2, 0, 5, 3, 4, 7, 2, 2, 0, 5, 3, 4, 7, 2, 2, 0
            ]
        }, {

    """
    print('---------- series ----------')
    print('[')

    for classification in per_day_count_by_classification:
        classification_name = next(iter(classification.keys()))

        data = ''
        for word_count in classification[classification_name]:
            data += f'{word_count},'

        print('{')
        print(f"  name: '{classification_name}',")
        print('  data: [')
        print(f'    {data}')
        print('        ]')
        print('},')

    print(']')
    return favorites


def get_all_tweets(screen_name):
    # Twitter only allows access to a users most recent 3240 tweets with this method

    # authorize twitter, initialize tweepy
    api = get_api()

    # initialize a list to hold all the tweepy Tweets
    alltweets = []

    # make initial request for most recent tweets (200 is the maximum allowed count)
    new_tweets = api.user_timeline(screen_name=screen_name, count=200, max_id=None)

    # save most recent tweets
    alltweets.extend(new_tweets)

    # save the id of the oldest tweet less one
    oldest = alltweets[-1].id - 1

    # keep grabbing tweets until there are no tweets left to grab
    while len(new_tweets) > 0:
        print("getting tweets before %s" % (oldest))

        # all subsiquent requests use the max_id param to prevent duplicates
        new_tweets = api.user_timeline(screen_name=screen_name, count=200, max_id=oldest)

        # save most recent tweets
        alltweets.extend(new_tweets)

        # update the id of the oldest tweet less one
        oldest = alltweets[-1].id - 1

        print("...%s tweets downloaded so far" % (len(alltweets)))

    # transform the tweepy tweets into a 2D array that will populate the csv
    outtweets = [[tweet.id_str, tweet.created_at, tweet.text.encode("utf-8")] for tweet in alltweets]

    # write the csv
    with open('%s_tweets.csv' % screen_name, 'w') as f:
        writer = csv.writer(f)
        writer.writerow(["id", "created_at", "text"])
        writer.writerows(outtweets)

    return outtweets
