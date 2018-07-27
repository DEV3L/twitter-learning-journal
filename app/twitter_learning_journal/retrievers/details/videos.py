def get_videos(tweets):
    videos = [tweet for tweet in tweets
              if tweet.full_text.lower().startswith('watched:')
              or 'via @YouTube' in tweet.full_text
              ]

    for video in videos:
        print(video)

    return videos
