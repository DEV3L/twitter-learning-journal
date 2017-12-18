from tweepy import Cursor

from app.twitter_learning_journal.models.favorite import Favorite


class Favorites:
    def __init__(self, twitter_api, screen_name):
        self._twitter_api = twitter_api
        self.screen_name = screen_name

    def get(self):
        favorites = []
        for favorite_response in self._call():
            favorite_model = Favorite(
                id=favorite_response.id,
                created_at=favorite_response.created_at,
                full_text=favorite_response.full_text,
                hashtags='|'.join([hashtag['text'] for hashtag in favorite_response.entities['hashtags']])
            )

            favorites.append(favorite_model)

        return favorites

    def _call(self):
        yield from Cursor(self._twitter_api.favorites, self.screen_name, tweet_mode='extended', count=200).items()
