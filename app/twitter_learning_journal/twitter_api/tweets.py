from tweepy import API
from tweepy import Cursor

from app.twitter_learning_journal.models.tweet import Tweet


class Tweets:
    def __init__(self, twitter_api: 'API', screen_name: str, *, tweet_type: str = 'favorite'):
        self.tweet_type = tweet_type
        self.screen_name = screen_name

        self._twitter_api = twitter_api
        self._twitter_api_type = twitter_api.favorites if 'favorite' == tweet_type else twitter_api.user_timeline

    def get(self):
        tweets = []
        for call_response in self._call():
            # this mapping logic could be extracted
            full_text = call_response.full_text

            if hasattr(call_response, 'retweeted_status'):
                full_text = call_response.retweeted_status.full_text

            tweet_model = Tweet(
                id=call_response.id,
                created_at=call_response.created_at,
                full_text=full_text,
                hashtags=self.extract_hashtags(call_response),
                type=self.tweet_type
            )

            tweets.append(tweet_model)

        return tweets

    @staticmethod
    def extract_hashtags(call_response):
        return '|'.join([hashtag['text'] for hashtag in call_response.entities['hashtags']])

    def _call(self):
        yield from Cursor(self._twitter_api_type, self.screen_name, tweet_mode='extended', count=200).items()
