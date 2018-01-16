from tweepy import API

from app.twitter_learning_journal.retrievers.twitter.tweets import Tweets


class TwitterRetriever():
    def __init__(self, api: API, screen_name: str, is_favorite: bool = False):
        self.api = api
        self.screen_name = screen_name
        self.is_favorite = is_favorite
        self._tweet_type = 'favorite' if is_favorite else 'tweet'

    def collect(self):
        tweets = Tweets(self.api, self.screen_name, tweet_type=self._tweet_type)
        return tweets.get()

    pass


"""

   # extract
    api = get_api()
    tweets = collect(api, screen_name, tweet_type='tweet')
    favorites = collect(api, screen_name)

    save_tweets(tweet_dao, favorites)
    save_tweets(tweet_dao, tweets)


"""
