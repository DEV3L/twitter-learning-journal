from datetime import datetime

from app.twitter_learning_journal.dao.tweet_dao import TweetDao
from app.twitter_learning_journal.models.detail import Detail
from app.twitter_learning_journal.transformers.transform_str import remove_ignore_characters_from_str
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


def create_detail(tweet):
    title = tweet.urls or input('Detail title: ').lower()
    full_text_without_ignore_characters = remove_ignore_characters_from_str(tweet.full_text.lower())

    if tweet.urls and full_text_without_ignore_characters.startswith('listened to'):
        lines = full_text_without_ignore_characters.splitlines()
        title = ' '.join(lines[0].replace('listened to', '').split()).strip()

    detail = Detail(title=title)
    detail.tweet_id = tweet.id
    detail.start_date = tweet.created_at
    detail.stop_date = tweet.created_at
    detail.title = title
    detail.url = tweet.urls
    detail.is_fully_classified = True

    if 'listened to' in tweet.full_text.lower():
        detail.type = 'audio'
        detail.word_count = 45
    else:
        detail.type = 'blog'
        detail.word_count = 500

    detail.classification = tweet.classification

    database.add(detail)

    return detail

if __name__ == '__main__':
    database = make_database()
    tweet_dao = TweetDao(database)

    print('Detail trainer: Iterate through all non fully classified Tweets')
    _tweets = tweet_dao.query_all()

    print(f'Total Tweets: {len(_tweets)}')

    _tweets = [tweet for tweet in _tweets if not tweet.is_fully_classified]
    _tweets = [tweet for tweet in _tweets if tweet.type == 'tweet']
    _tweets = sorted(_tweets, key=lambda x: x.created_at, reverse=True)
    _details = database.query(Detail).all()

    total = len(_tweets)

    print(f'Total Tweets Not Fully Classified: {total}')
    keywords = ['read', 'listen', 'listened', 'listened to', 'watched', 'watch']

    total_processed = 0
    total_details = 0

    for tweet in _tweets:
        has_keywords = False
        has_quoted_keywords = False
        _full_text_original = tweet.full_text
        _full_text = ' '.join(remove_ignore_characters_from_str(tweet.full_text).split()).lower()

        print('-----TWEET-----')
        print(f' classification: {tweet.classification}')
        print(f' url: {tweet.urls}')
        print(f' {tweet.full_text}')

        for keyword in keywords:
            if keyword in _full_text:
                has_keywords = True

            if f'"{keyword}"' in _full_text or f"'{keyword}'" in _full_text:
                has_quoted_keywords = True

        if has_keywords and not has_quoted_keywords:
            # handle these later
            # books, audio, videos
            print()  # breakpoint for debugger to hit
            continue
        elif not tweet.urls:
            print('No details for tweet')
            print('processed')
            tweet.is_fully_classified = True
        else:
            detail = create_detail(tweet)
            print(f'Detail created: {detail}')

            total_details += 1

            tweet.is_fully_classified = True

        database.commit()
        total_processed += 1

        # has_triggers = has_triggers or (trigger in tweet.full_text)
        #         has_quoted_triggers = has_quoted_triggers and (f"'{trigger}'" not in tweet.full_text)
        #     if not has_triggers and not tweet.urls:
        #         print('Auto Processed!')
        #         command = 'p'
        #     elif has_triggers and has_quoted_triggers and not tweet.urls:
        #         print('Auto Processed!')
        #         command = 'p'
        #     else:
        #         command = 'a'

        pass

    # print('Commands:\n'
    #       ' - (e)xit\n'
    #       ' - (s)kip\n'
    #       ' - (p)rocessed\n'
    #       ' - (d)details\n'
    #       ' - (a)dd or update to Tweet\n'
    #       ' else continue')
    #
    # commands = {
    #     'e', 's', 'p', 'd', 'a'
    # }
    #
    # is_exit = False
    # tweet_count = 0
    # details_added = 0
    # command = input('Command: ').lower()
    #
    # for tweet in _tweets:
    #     print(f'\n--------\nClassification:\n{tweet.classification}')
    #     print(f'Full Text:\n{tweet.full_text}' + (f'\nURLs:{tweet.urls}' if tweet.urls else ''))
    #
    #     if is_exit:
    #         break
    #
    #     if tweet_count >= 10:
    #         print()
    #         tweet_count = 0
    #
    #     tweet_count += 1
    #     # Thinking about accounting for audio books next...
    #     #
    #     # I always post 'started listening to' and 'stopped listening to' for Audible books
    #     #
    #     # Overlay distribution of words...
    #     # total audio length / number days = daily average audio
    #     # daily average audio * avg spoke words per minute = words
    #     trigger_words = ['read', 'listen', 'listened', 'listened to']
    #
    #     # command = None
    #
    #     has_triggers = False
    #     has_quoted_triggers = False
    #
    #     for trigger in trigger_words:
    #         has_triggers = has_triggers or (trigger in tweet.full_text)
    #         has_quoted_triggers = has_quoted_triggers and (f"'{trigger}'" not in tweet.full_text)
    #     if not has_triggers and not tweet.urls:
    #         print('Auto Processed!')
    #         command = 'p'
    #     elif has_triggers and has_quoted_triggers and not tweet.urls:
    #         print('Auto Processed!')
    #         command = 'p'
    #     else:
    #         command = 'a'
    #
    #     if tweet.is_fully_classified:
    #         print('Auto Processed!')
    #         command = 'p'
    #
    #     while True:
    #         if details_added >= 10:
    #             print()
    #             details_added = 0
    #         print(f'Classification:\n{tweet.classification}')
    #         print(f'Full Text:\n{tweet.full_text}' + (f'\nURLs:{tweet.urls}' if tweet.urls else ''))
    #
    #         if has_triggers:
    #             print()
    #
    #         command = command or input('Command: ').lower()
    #
    #         if command not in commands:  #
    #             command = None
    #             print(f'"{command}" is not a valid command')
    #         elif 's' == command:  #
    #             command = None
    #         elif 'd' == command:
    #             for detail in _details:
    #                 print(str(detail))
    #             command = None
    #         elif 'e' == command:  #
    #             is_exit = True
    #         elif 'p' == command:  #
    #             tweet.is_fully_classified = True
    #             tweet_dao.add(tweet)
    #             database.commit()
    #             print('Tweet marked as full classified!')
    #         elif 'a' == command:
    #             title = tweet.urls or input('Detail title: ').lower()
    #             cleaned_full_text = remove_ignore_characters_from_str(tweet.full_text.lower())
    #
    #             like_details = [detail for detail in _details if title in detail.title]
    #             related_detail = None
    #
    #             is_skip = False
    #
    #             for detail in like_details:
    #                 print(str(detail))
    #                 is_detail = bool(input('Is this your detail? '))
    #                 if is_detail:
    #                     if detail.is_fully_classified:
    #                         is_skip = bool(input('Detail is fully classified, skip? '))
    #                         if is_skip:
    #                             break
    #
    #                     related_detail = detail
    #
    #             if is_skip:
    #                 is_processed = bool(input('Is Tweet processed? '))
    #                 command = 'p'
    #                 continue
    #
    #             if not related_detail:
    #                 if tweet.urls and cleaned_full_text.startswith('listened to'):
    #                     lines = cleaned_full_text.splitlines()
    #                     title = ' '.join(lines[0].replace('listened to', '').split()).strip()
    #
    #                 details_added += 1
    #                 related_detail = Detail(title=title)
    #                 related_detail.tweet_id = tweet.id
    #                 related_detail.start_date = tweet.created_at
    #                 related_detail.stop_date = tweet.created_at
    #                 related_detail.title = title
    #                 related_detail.url = tweet.urls
    #                 related_detail.is_fully_classified = True
    #
    #                 if 'listened to' in tweet.full_text.lower():
    #                     related_detail.type = 'audio'
    #                     related_detail.word_count = 45
    #                 else:
    #                     related_detail.type = 'blog'
    #                     related_detail.word_count = 500
    #
    #                 related_detail.classification = tweet.classification
    #                 tweet.is_fully_classified = True
    #                 database.add(tweet)
    #                 database.add(related_detail)
    #                 database.commit()
    #                 print(f'Detail created: {related_detail}')
    #                 print('Tweet marked as full classified!')
    #
    #             # print(f'Detail:{related_detail}')
    #             # if bool(input('Done? ')):
    #             #     continue
    #             #
    #             # while True:
    #             #     print('Input blank to not update')
    #             #     print(f'Detail:{related_detail}')
    #             #
    #             #     print(f'start_date:{related_detail.start_date}')
    #             #     related_detail.start_date = get_input_value(is_date=True) or related_detail.start_date
    #             #
    #             #     print(f'stop_date:{related_detail.stop_date}')
    #             #     related_detail.stop_date = get_input_value(is_date=True) or related_detail.stop_date
    #             #
    #             #     print(f'type:{related_detail.type}')
    #             #     related_detail.type = get_input_value() or related_detail.type
    #             #
    #             #     print(f'title:{related_detail.title}')
    #             #     related_detail.title = get_input_value() or related_detail.title
    #             #
    #             #     print(f'url:{related_detail.url}')
    #             #     related_detail.url = get_input_value() or related_detail.url
    #             #
    #             #     print(f'word_count:{related_detail.word_count}')
    #             #     related_detail.word_count = get_input_value(is_int=True) or related_detail.word_count
    #             #
    #             #     print(f'classification:{related_detail.classification}')
    #             #     related_detail.classification = get_input_value() or related_detail.classification
    #             #
    #             #     print(f'is_fully_classified:{related_detail.is_fully_classified}')
    #             #     related_detail.is_fully_classified = get_input_value(
    #             #         is_bool=True) or related_detail.is_fully_classified
    #             #
    #             #     if bool(input('Done? ')):
    #             #         database.commit()
    #             #         break
    #
    #
    #         break

    print(total_processed)

    database.commit()
    print('Done')
