def get_videos(tweets):
    videos = [tweet for tweet in tweets
              if tweet.full_text.lower().startswith('watched:')]

    for video in videos:
        print(video)

    return videos
