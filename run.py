from tweet_dumper import classify_favorites, timeline

if __name__ == '__main__':
    screen_name = 'dev3l_'

    # only need once to save favorites
    # favorites = collect_favorites(screen_name)
    # write_favorites(favorites)

    classify_favorites()
    timeline()

    # to be refined
    # get_all_tweets(sceen_name)
