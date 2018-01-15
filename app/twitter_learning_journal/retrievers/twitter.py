class TwitterRetriever():
    def __init__(self, api, screen_name, is_favorite=False):
        self.api = api
        self.screen_name = screen_name
        self.is_favorite = is_favorite

    # def collect(screen_name, *, tweet_type='favorite'):
    #     tweets = Tweets(api, screen_name, tweet_type=tweet_type)
    #     return tweets.get()

    pass


"""

   # extract
    api = get_api()
    tweets = collect(api, screen_name, tweet_type='tweet')
    favorites = collect(api, screen_name)

    save_tweets(tweet_dao, favorites)
    save_tweets(tweet_dao, tweets)


"""
