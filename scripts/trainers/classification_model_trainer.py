from app.twitter_learning_journal.classifiers import get_classification_model
from app.twitter_learning_journal.classifiers.word_classifier import WordClassifier
from app.twitter_learning_journal.dao.tweet_dao import TweetDao
from app.twitter_learning_journal.database.sqlalchemy_database import Database

if __name__ == '__main__':
    database = Database()
    tweet_dao = TweetDao(database)

    _tweets = tweet_dao.query_all()
    total = len(_tweets)

    classification_model = get_classification_model(None)  # global

    print(f'Total Tweets: {total}')

    for count, tweet in enumerate(_tweets):
        if not tweet.hashtags:
            continue

        print(f'{count} of {total}')

        for hashtag in tweet.hashtags.split('|'):
            _hashtag = hashtag.lower().strip()
            word_classifier = WordClassifier(_hashtag, classification_model)
            classification = word_classifier.classify()

            if not sum([classification[key] for key in classification.keys()]):
                print(f'Not classified: {_hashtag}')
                print(f'            - : {tweet.full_text}\n')

                tag = input('Enter classification tag: ')
                tag = tag.lower().strip()

                if tag not in classification_model:
                    print(f'Adding classification tag: {tag}')
                    classification_model[tag] = set()

                classification_model[tag].add(_hashtag)

                print(classification_model[tag])
