def get_pairings(tweets):
    pairings = [tweet for tweet in tweets
                if tweet.full_text.lower().startswith('#strongstylepair')
                or tweet.full_text.lower().startswith('practiced #python')
                ]

    for pairing in pairings:
        print(pairing)

    return pairings
