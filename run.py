from app.twitter_learning_journal.database.sqlalchemy_database import Database
from tweet_dumper import timeline, collect, save_tweets, build_tables, classify_tweets, classify_audible_books

if __name__ == '__main__':
    screen_name = 'dev3l_'

    build_tables(Database())

    favorites = collect(screen_name)
    tweets = collect(screen_name, tweet_type='tweets')

    save_tweets(favorites)
    save_tweets(tweets)

    classify_tweets()
    books = classify_audible_books()

    timeline(books)
