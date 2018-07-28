def get_conferences(tweets):
    conferences = [tweet for tweet in tweets
                   if tweet.full_text.lower().startswith("i'm at")
                   or tweet.full_text.lower().startswith('attending:')
                   or tweet.full_text.lower().startswith('attended:')
                   or tweet.full_text.lower().startswith('extreme fake it till you make it')
                   ]

    for conference in conferences:
        print(conference)

    return conferences
