from tweepy import API
from tweepy import Cursor

from app.twitter_learning_journal.models.tweet import Tweet
from app.twitter_learning_journal.twitter_api.tweet_cache_loader import TweetCacheLoader
from app.twitter_learning_journal.twitter_api.tweet_cacher import TweetCacher


class Tweets:
    def __init__(self, twitter_api: API, screen_name: str, *, tweet_type: str = 'favorite'):
        self.tweet_type = tweet_type
        self.screen_name = screen_name

        self._twitter_api = twitter_api
        self._twitter_api_type = twitter_api.favorites if 'favorite' == tweet_type else twitter_api.user_timeline
        self._cached_tweets = None

    @property
    def cached_tweets(self):
        if self._cached_tweets is not None:
            return self._cached_tweets

        tweet_cache_loader = TweetCacheLoader(self.screen_name)
        self._cached_tweets = tweet_cache_loader.load_cached_tweets()

        return self._cached_tweets

    def get(self):
        tweets = []

        for call_response in self._call():
            tweet_model = self._get_tweet(call_response)

            if tweet_model in self.cached_tweets:
                break

            TweetCacher(self.screen_name, tweet_model).cache()
            tweets.append(tweet_model)

        return self.merge_lists(tweets, self.cached_tweets)

    def _call(self):
        yield from Cursor(self._twitter_api_type, self.screen_name, tweet_mode='extended', count=50).items()

    def _get_tweet(self, call_response):
        full_text = self.extract_full_text(call_response)
        urls = self.extract_urls(call_response)
        tweet_model = Tweet(
            id=call_response.id,
            created_at=call_response.created_at,
            full_text=full_text,
            hashtags=self.extract_hashtags(call_response),
            urls='|'.join(urls),
            type=self.tweet_type
        )

        return tweet_model

    @staticmethod
    def merge_lists(list_one: list, list_two: list):
        merged_list = []
        merged_list.extend(list_one)

        list_two_only = [_object for _object in list_two if _object not in merged_list]
        merged_list.extend(list_two_only)

        return merged_list

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
