from datetime import datetime

from app.twitter_learning_journal.dao.tweet_dao import TweetDao
from app.twitter_learning_journal.models.detail import Detail
from scripts.trainers.script_dependencies import make_database


def get_input_value(*, is_date=False, is_bool=False, is_int=False):
    update_value = input('Enter new value: '
                         '(yyyy-mm-dd) ' if is_date else '')
    update_value = update_value.strip()

    if update_value:
        if is_date:
            try:
                update_value = datetime.strptime(update_value, '%Y-%m-%d')
            except:
                print(f'Start date "{update_value}" not in "yyyy-mm-dd" format')
                return
        elif is_bool:
            update_value = bool(update_value)
        elif is_int:
            update_value = int(update_value)

    return update_value


if __name__ == '__main__':
    database = make_database()
    tweet_dao = TweetDao(database)

    _tweets = tweet_dao.query_all()
    _tweets = [tweet for tweet in _tweets if not tweet.is_fully_classified]
    _tweets = [tweet for tweet in _tweets if tweet.type == 'tweet']
    _tweets = sorted(_tweets, key=lambda x: x.created_at, reverse=True)
    _details = database.query(Detail).all()

    total = len(_tweets)

    print('Detail trainer: Iterate through all non fully classified Tweets')
    print(f'Total Tweets Not Fully Classified: {total}')
    print('Commands:\n'
          ' - (e)xit\n'
          ' - (s)kip\n'
          ' - (p)rocessed\n'
          ' - (d)details\n'
          ' - (a)dd or update to Tweet\n'
          ' else continue')

    commands = {
        'e', 's', 'p', 'd', 'a'
    }

    is_exit = False
    for tweet in _tweets:
        if is_exit:
            break

        while True:
            print(f'Classification:\n{tweet.classification}')
            print(f'Full Text:\n{tweet.full_text}')

            command = input('Command: ').lower()

            if command not in commands:  #
                print(f'"{command}" is not a valid command')
                continue
            elif 'e' == command:  #
                is_exit = True
            elif 's' == command:  #
                pass
            elif 'p' == command:  #
                tweet.is_fully_classified = True
                tweet_dao.add(tweet)
                database.commit()
                print('Tweet marked as full classified!')
            elif 'd' == command:
                for detail in _details:
                    print(str(detail))
                continue
            elif 'a' == command:
                title = input('Detail title: ').lower()

                like_details = [detail for detail in _details if title in detail.title]
                related_detail = None

                is_skip = False

                for detail in like_details:
                    print(str(detail))
                    is_detail = bool(input('Is this your detail? '))
                    if is_detail:
                        if detail.is_fully_classified:
                            is_skip = bool(input('Detail is fully classified, continue? '))
                            if is_skip:
                                break

                        related_detail = detail

                if is_skip:
                    continue

                if not related_detail:
                    if bool(input(f'Detail of title: "{title}" not found, Add one? ')):
                        related_detail = Detail(title=title)
                        related_detail.tweet_id = tweet.id
                        related_detail.start_date = tweet.created_at
                        related_detail.stop_date = tweet.created_at
                        related_detail.title = title
                        related_detail.is_fully_classified = True

                        if 'listened to' in tweet.full_text.lower():
                            related_detail.type = 'audio'
                            related_detail.word_count = 45
                        else:
                            related_detail.type = 'blog'
                            related_detail.word_count = 500

                        related_detail.classification = tweet.classification
                        database.add(related_detail)
                        database.commit()
                    else:
                        continue

                while True:
                    print('Input blank to not update')
                    print(f'Detail:{related_detail}')

                    print(f'start_date:{related_detail.start_date}')
                    related_detail.start_date = get_input_value(is_date=True) or related_detail.start_date

                    print(f'stop_date:{related_detail.stop_date}')
                    related_detail.stop_date = get_input_value(is_date=True) or related_detail.stop_date

                    print(f'type:{related_detail.type}')
                    related_detail.type = get_input_value() or related_detail.type

                    print(f'title:{related_detail.title}')
                    related_detail.title = get_input_value() or related_detail.title

                    print(f'url:{related_detail.url}')
                    related_detail.url = get_input_value() or related_detail.url

                    print(f'word_count:{related_detail.word_count}')
                    related_detail.word_count = get_input_value(is_int=True) or related_detail.word_count

                    print(f'classification:{related_detail.classification}')
                    related_detail.classification = get_input_value() or related_detail.classification

                    print(f'is_fully_classified:{related_detail.is_fully_classified}')
                    related_detail.is_fully_classified = get_input_value(
                        is_bool=True) or related_detail.is_fully_classified

                    if bool(input('Done? ')):
                        database.commit()
                        break
                continue
            break

    database.commit()
    print('Done')
