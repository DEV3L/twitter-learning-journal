#!/usr/bin/env python
# encoding: utf-8

"""
This is my 'hacker-mode' file!

It has been stitched together from a few github gist files
"""

# https://gist.github.com/yanofsky/5436496
# https://gist.github.com/datagrok/74a71f572493e603919e

from app.twitter_learning_journal.database.sqlalchemy_database import Database
from app.twitter_learning_journal.models import Base
from app.twitter_learning_journal.models.favorite import Favorite
from app.twitter_learning_journal.twitter_api.api import get_api
from app.twitter_learning_journal.twitter_api.favorites import Favorites


def get_all_tweets(screen_name):
    # Twitter only allows access to a users most recent 3240 tweets with this method

    # authorize twitter, initialize tweepy
    api = get_api()

    # initialize a list to hold all the tweepy Tweets
    alltweets = []

    # make initial request for most recent tweets (200 is the maximum allowed count)
    # new_tweets = api.user_timeline(screen_name=screen_name, count=200, max_id=None)
    #
    # # save most recent tweets
    # alltweets.extend(new_tweets)
    #
    # # save the id of the oldest tweet less one
    # oldest = alltweets[-1].id - 1
    #
    # # keep grabbing tweets until there are no tweets left to grab
    # while len(new_tweets) > 0:
    #     print("getting tweets before %s" % (oldest))
    #
    #     # all subsiquent requests use the max_id param to prevent duplicates
    #     new_tweets = api.user_timeline(screen_name=screen_name, count=200, max_id=oldest)
    #
    #     # save most recent tweets
    #     alltweets.extend(new_tweets)
    #
    #     # update the id of the oldest tweet less one
    #     oldest = alltweets[-1].id - 1
    #
    #     print("...%s tweets downloaded so far" % (len(alltweets)))
    #
    # # transform the tweepy tweets into a 2D array that will populate the csv
    # outtweets = [[tweet.id_str, tweet.created_at, tweet.text.encode("utf-8")] for tweet in alltweets]

    favorites = Favorites(api, screen_name)
    favorites_list = favorites.get()

    # # write the csv
    # with open('%s_tweets.csv' % screen_name, 'w') as f:
    #     writer = csv.writer(f)
    #     writer.writerow(["id", "created_at", "text"])
    #     writer.writerows(outtweets)

    database = Database()
    Base.metadata.create_all(database._engine)

    for favorite in favorites_list:
        _favorite = database.query(Favorite).filter(Favorite.id == favorite.id).first()

        if not _favorite:
            database.add(favorite)

    # sql_favorites_list = database.query(Favorite).all()
    # for favorite in sql_favorites_list:
    #     print(favorite)

    database.commit()

    return favorites_list
