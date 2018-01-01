from collections import defaultdict
from datetime import datetime, timedelta

from app.twitter_learning_journal.classifiers import global_classification_model
from app.twitter_learning_journal.transformers.transform_datetime import transform_datetime_to_iso_date_str


def _add_tweets_to_timeline(tweets, timeline):
    for tweet in tweets:
        timeline[transform_datetime_to_iso_date_str(tweet.created_at)].append(tweet)


def _count_tweet_words(tweets):
    tweet_words = 0
    for tweet in tweets:
        tweet_words += tweet.word_count
    return tweet_words


def create_timeline(start_date, stop_date, tweets: list, details: list, audio_books: list, books: list):
    timeline = build_timeline(start_date, stop_date)

    tweet_count = len(tweets)
    tweet_words = _count_tweet_words(tweets)

    audio_books_words = len(audio_books)
    total_audio_books = 0

    books_words = len(books)
    total_books = 0

    blog_words = 0
    total_blogs = 0

    podcast_words = 0
    total_podcasts = 0

    _add_tweets_to_timeline(tweets, timeline)
    per_day_count_by_classification = _create_per_day_count_by_classification()

    classification_counts = defaultdict(int)

    audio_book_days = defaultdict(int)

    for detail in details:
        if detail.type == 'podcast':
            total_podcasts += 1
            podcast_words += detail.word_count
        elif detail.type != 'blog':
            continue
        else:
            total_blogs += 1
            blog_words += detail.word_count

    for key in sorted(timeline.keys()):
        tweets = [tweet for tweet in timeline[key]]
        key_date = datetime.strptime(key, '%Y-%m-%d')
        count = len(timeline[key])

        classification_values = defaultdict(int)

        for tweet in tweets:
            classification_value = tweet.classification

            if not classification_value:
                classification_value = 'not_classified'

            classification_values[classification_value] += tweet.word_count

        for audio_detail in audio_books:
            if key_date >= audio_detail.start_date and key_date <= audio_detail.stop_date:
                total_days = (audio_detail.stop_date - audio_detail.start_date).days
                audio_book_days[audio_detail.title] += 1

                """
                https://www.quora.com/Speeches-For-the-average-person-speaking-at-a-normal-pace-what-is-the-typical-number-of-words-they-can-say-in-one-minute
                "publishers recommend books on tape to be voiced at 150-160 wpm"
                """
                words_per_minute = 125  # well below stated suggestion
                total_words = words_per_minute * audio_detail.total_audio_minutes

                average_words_per_day = total_words / total_days
                audio_books_words += average_words_per_day
                classification_counts[audio_detail.classification] += average_words_per_day
                classification_values[audio_detail.classification] += average_words_per_day

        for detail in [detail for detail in details if detail.is_fully_classified]:
            if detail.start_date is not None and \
                            detail.stop_date is not None and \
                            detail.word_count is not None:

                print(
                    f'type:{detail.type}, start_date:{detail.start_date.date()}, '
                    f'stop_date:{detail.stop_date.date()}, key_date:{key_date.date()}')

                if (detail.start_date.date() <= key_date.date() <= detail.stop_date.date()):
                    total_days = (detail.stop_date - detail.start_date).days
                    total_days += 1

                    word_count = detail.word_count or 0
                    total_words = word_count

                    if detail.type == 'audio':
                        """
                        https://www.quora.com/Speeches-For-the-average-person-speaking-at-a-normal-pace-what-is-the-typical-number-of-words-they-can-say-in-one-minute
                        "publishers recommend books on tape to be voiced at 150-160 wpm"
                        """
                        words_per_minute = 10  # 125  # well below stated suggestion
                        total_words = words_per_minute * word_count

                    average_words_per_day = total_words / total_days
                    classification_values[detail.classification] += average_words_per_day

        display_str = ''
        for _key, value in classification_values.items():
            if display_str:
                display_str += ','

            display_str += f'{_key}={value}'

        for classification in per_day_count_by_classification:
            classification_name = next(iter(classification.keys()))
            classification_count = classification_values.get(classification_name)
            classification[classification_name].append(classification_count or 0)

        print(f'date={key}:tweets_count={count}:total_words={word_count}|classifications:{display_str}')

    _audio_books = []

    for audio_detail in audio_books:
        if not audio_detail.title in audio_book_days.keys():
            continue

        days = audio_book_days[audio_detail.title]

        total_days = (audio_detail.stop_date - audio_detail.start_date).days
        total_days += 1

        book_parts = days / total_days
        total_audio_books += book_parts
        _audio_books.append((audio_detail.title, audio_detail.start_date, audio_detail.stop_date))

    print('categories =')
    print('[')
    for key in sorted(timeline.keys()):
        if datetime.strptime(key, '%Y-%m-%d') < start_date \
                or datetime.strptime(key, '%Y-%m-%d') > stop_date:
            continue
        print(f"'{key}',")
    print('];')

    print('series =')
    print('[')

    for classification in per_day_count_by_classification:
        classification_name = next(iter(classification.keys()))

        if sum(classification[classification_name]) == 0:
            continue

        data = ''
        classifcation_total_words = 0
        for word_count in classification[classification_name]:
            classifcation_total_words += word_count
            data += f'{word_count},'

        classification_counts[classification_name] += classifcation_total_words

        print('{')
        print(f"  name: '{classification_name}',")
        print('  data: [')
        print(f'    {data}')
        print('        ]')
        print('},')

    print('];')

    print('---------- data aggregates data ----------')
    print('<div>')
    print('  <div style="float: left;">')
    print('    <table border="border">')
    print('      <thead>Consumption by Type</thead>')
    print('      <tr><th>type</th><th>count</th></tr>')
    print(f'      <tr><td>Twitter Tweets & Favorites</td><td>{tweet_count}</td></tr>')
    print(f'       <tr><td>Blogs</td><td>{total_blogs}</td></tr>')
    print(f'       <tr><td>Podcasts</td><td>{total_podcasts}</td></tr>')
    print(f'       <tr><td>Audio Books</td><td>{total_audio_books:.2f}</td></tr>')
    print('    </table>')
    print('  </div>')
    print('  <div style="float: left; padding-left: 50pt">')
    print('    <table border="border">')
    print('      <thead>Words by Type</thead>')
    print('      <tr><th>type</th><th>count</th></tr>')
    print(f'      <tr><td>Twitter</td><td>{tweet_words}</td></tr>')
    print(f'       <tr><td>Blogs</td><td>{blog_words}</td></tr>')
    print(f'       <tr><td>Podcasts</td><td>{podcast_words}</td></tr>')
    print(f'       <tr><td>Audio Books</td><td>{int(audio_books_words)}</td></tr>')
    print('    </table>')
    print('  </div>')
    print('  <div style="float: left; padding-left: 50pt">')
    print('    <table border="border">')
    print('      <thead>Consumption by ''Word'' count</thead>')
    print('      <tr><th>type</th><th>count</th></tr>')

    for classification, value in classification_counts.items():
        print(f'      <tr><td>{classification}</td><td>{int(value)}</td></tr>')

    print(f'      <tr><th>total</th><td>{int(sum(classification_counts.values()))}</td></tr>')
    print('    </table>')
    print('  </div>')

    print('  <div style="float: left; padding-left: 50pt">')
    print('    <table border="border">')
    print('      <thead>Audio Books</thead>')
    print('      <tr><th>title</th><th>start</th><th>stop</th></tr>')

    for audio_book in _audio_books:
        print(f'      <tr><td>{audio_book[0]}</td><td>{audio_book[1].date()}</td><td>{audio_book[2].date()}</td></tr>')

    print('    </table>')
    print('  </div>')

    print('</div>')

    return tweets


def _create_per_day_count_by_classification():
    per_day_count_by_classification = []
    for key in sorted(global_classification_model.keys()):
        per_day_count_by_classification.append({key: []})
    return per_day_count_by_classification


def build_timeline(min_date, max_date):
    _timeline = defaultdict(list)
    _start_date = datetime(min_date.year, min_date.month, min_date.day)

    while _start_date < max_date:
        _timeline[transform_datetime_to_iso_date_str(_start_date)] = []
        _start_date += timedelta(days=1)

    return _timeline
