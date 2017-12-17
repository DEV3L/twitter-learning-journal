#!/usr/bin/env python
# encoding: utf-8

"""
This is my 'hacker-mode' file!

It has been stitched together from a few github gist files
"""

# https://gist.github.com/yanofsky/5436496
# https://gist.github.com/datagrok/74a71f572493e603919e

import csv
import json

import tweepy  # https://github.com/tweepy/tweepy

from app.twitter_learning_journal.dao import os_env

consumer_key = os_env.os_environ('TWITTER_CONSUMER_KEY')
consumer_secret = os_env.os_environ('TWITTER_CONSUMER_SECRET')
access_token = os_env.os_environ('TWITTER_ACCESS_TOKEN')
access_token_secret = os_env.os_environ('TWITTER_TOKEN_SECRET')


def get_api():
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    return tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)


def get_unseen_statuses(api, min_id, max_id, screen_name):
    if min_id and max_id:
        yield from tweepy.Cursor(api.favorites, screen_name,
                                 count=200, since_id=max_id, include_entities=True).items()
        yield from tweepy.Cursor(api.favorites, screen_name,
                                 count=200, max_id=min_id, include_entities=True).items()
    else:
        yield from tweepy.Cursor(api.favorites, screen_name,
                                 count=200, include_entities=True).items()


def get_all_tweets(screen_name):
    # Twitter only allows access to a users most recent 3240 tweets with this method

    # authorize twitter, initialize tweepy
    api = get_api()

    # initialize a list to hold all the tweepy Tweets
    alltweets = []

    # make initial request for most recent tweets (200 is the maximum allowed count)
    new_tweets = api.user_timeline(screen_name=screen_name, count=200)

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

    likes = []
    for status in get_unseen_statuses(api, None, None, screen_name):
        print(status)
        print(json.dumps(status._json))
        likes.append(json.dumps(status._json))


    # write the csv
    with open('%s_tweets.csv' % screen_name, 'w') as f:
        writer = csv.writer(f)
        writer.writerow(["id", "created_at", "text"])
        writer.writerows(outtweets)

    with open('%s_likes.txt' % screen_name, 'w') as f:
        for like in likes:
            f.write(like + '\n')


if __name__ == '__main__':
    # pass in the username of the account you want to download
    get_all_tweets("dev3l_")
