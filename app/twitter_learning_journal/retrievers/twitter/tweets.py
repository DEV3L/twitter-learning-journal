from datetime import datetime

from tweepy import API
from tweepy import Cursor

from app.twitter_learning_journal.cachers.cache_loader import CacheLoader
from app.twitter_learning_journal.cachers.tweet_cacher import TweetCacher
from app.twitter_learning_journal.models.tweet import Tweet
from app.twitter_learning_journal.models.tweet_raw_data import TweetRawData
from app.twitter_learning_journal.services.pickle_service import serialize


class Tweets:
    def __init__(self, twitter_api: API, screen_name: str, *, tweet_type: str = 'favorite'):
        self.tweet_type = tweet_type
        self.screen_name = screen_name

        self._twitter_api = twitter_api
        self._twitter_api_type = twitter_api.favorites if 'favorite' == tweet_type else twitter_api.user_timeline
        self._cached_tweets = None
        self._realtime_rate_in_hours = 24

    @property
    def cached_tweets(self):
        if self._cached_tweets is not None:
            return self._cached_tweets

        tweet_cache_loader = CacheLoader(self.screen_name)
        self._cached_tweets = tweet_cache_loader.load_cached_entities()

        return self._cached_tweets

    def get(self):
        tweets = []

        if self.has_new_tweets():
            self._get_from_twitter(tweets)

        tweets.extend(self.cached_tweets)
        return tweets

    def has_new_tweets(self):
        if not self.cached_tweets:
            return True

        _cached_tweets = list(self.cached_tweets)
        _cached_tweets.sort(key=lambda tweet: tweet.created_at, reverse=True)

        most_recent_tweet = _cached_tweets[0]
        seconds_since_last_cached_tweet = (datetime.now() - most_recent_tweet.created_at).seconds
        hours_since_last_cached_tweet = (seconds_since_last_cached_tweet / 60) / 60

        return hours_since_last_cached_tweet > self._realtime_rate_in_hours

    def _get_from_twitter(self, tweets: list):
        for call_response in self._call():
            tweet_model = self._get_tweet(call_response)

            if tweet_model in self.cached_tweets:
                break

            TweetCacher(self.screen_name, tweet_model).cache()
            tweets.append(tweet_model)

    def _call(self):
        yield from Cursor(self._twitter_api_type, self.screen_name, tweet_mode='extended', count=50).items()

    def _get_tweet(self, call_response):
        full_text = self.extract_full_text(call_response)
        urls = self.extract_urls(call_response)


        tweet_model = Tweet(
            screen_name=self.screen_name,
            id=call_response.id,
            created_at=call_response.created_at,
            full_text=full_text,
            hashtags=self.extract_hashtags(call_response),
            urls='|'.join(urls),
            type=self.tweet_type,
        )

        pickled_response = serialize(call_response)
        raw_data = TweetRawData(tweet=tweet_model, raw_data=pickled_response)

        tweet_model.tweet_raw_data.append(raw_data)
        return tweet_model

    @staticmethod
    def extract_full_text(call_response):
        full_text = call_response.full_text
        if hasattr(call_response, 'retweeted_status'):
            full_text = call_response.retweeted_status.full_text
        return full_text

    @staticmethod
    def extract_hashtags(call_response):
        return '|'.join([hashtag['text'] for hashtag in call_response.entities['hashtags']])

    @staticmethod
    def extract_urls(call_response):
        urls = [url['expanded_url'] for url in call_response.entities['urls']]
        urls = Tweets._remove_ignore_urls(urls)

        if hasattr(call_response, 'retweeted_status'):
            if not urls:
                urls = [url['expanded_url'] for url in call_response.retweeted_status.entities['urls']]
                urls = Tweets._remove_ignore_urls(urls)

        return urls

    @staticmethod
    def _remove_ignore_urls(urls: list):
        ignore_twitter_urls = ['https://twitter.com/', 'https://github.com/']
        _urls = []

        for url in urls:
            found = False
            for ignore_url in ignore_twitter_urls:
                if ignore_url in url:
                    found = True
                    break

            if not found:
                _urls.append(url)
        return _urls
