#!/usr/bin/env python
# encoding: utf-8

"""
This is my 'hacker-mode' file!

It has been stitched together from a few github gist files
"""

# https://gist.github.com/yanofsky/5436496
# https://gist.github.com/datagrok/74a71f572493e603919e
from collections import defaultdict
from datetime import datetime, timedelta

from app.twitter_learning_journal.classifiers import global_classification_model, get_classification_model
from app.twitter_learning_journal.dao.tweet_dao import TweetDao
from app.twitter_learning_journal.models import Base
from app.twitter_learning_journal.models.detail import Detail
from app.twitter_learning_journal.services.tweets_processing_service import TweetsProcessingService
from app.twitter_learning_journal.transformers.transform_datetime import transform_datetime_to_iso_date_str
from app.twitter_learning_journal.transformers.transform_str import remove_ignore_characters_from_str
from app.twitter_learning_journal.twitter_api.tweets import Tweets


def build_tables(database):
    Base.metadata.create_all(database._engine)


def collect(api, screen_name, *, tweet_type='favorite'):
    tweets = Tweets(api, screen_name, tweet_type=tweet_type)
    return tweets.get()


def save_tweets(tweet_dao, tweets):
    for tweet in tweets:
        if not tweet_dao.exists(tweet.id):
            tweet_dao.add(tweet)

    tweet_dao.commit()


def classify_tweets(tweet_dao):
    tweets = tweet_dao.query_all()

    tweets_processing_service = TweetsProcessingService(tweets)
    tweets_processing_service.count_tweet_words()
    tweets_processing_service.classify_tweets()

    tweet_dao.add_all(tweets_processing_service.tweets)
    tweet_dao.commit()


def add_sub_classification_to_models(tweet_dao):
    tweets = tweet_dao.query_all()

    unclassified_tweets = [tweet for tweet in tweets if not tweet.classification]
    classified_tweets = [tweet for tweet in tweets if tweet.classification]

    sub_classification_model = dict(get_classification_model(None))

    for tweet in classified_tweets:
        cleaned_full_text = remove_ignore_characters_from_str(tweet.full_text)
        updated_classification = sub_classification_model[tweet.classification].union(cleaned_full_text)
        sub_classification_model[tweet.classification] = updated_classification

    tweets_processing_service = TweetsProcessingService(unclassified_tweets,
                                                        classification_model=sub_classification_model,
                                                        weight_text=.1, weight_hashtag=.5)
    tweets_processing_service.classify_tweets()

    tweet_dao.add_all(tweets_processing_service.tweets)
    tweet_dao.commit()


# results = [
#         ('Books', 0, 0, 0),
#         ('Audio Books', 1.86, 101250, 0),
#         ('Podcasts', 19, 111479, 0),
#         ('Blogs', 123, 219572, 0),
#         ('Tweets & Favorites', 319, 36474, 0),
#         ('TOTAL', '-', 429391, 0),
#     ]

def _process_books(books, timeline):
    for book in books:
        pass


def timeline(tweet_dao: TweetDao, details: list, audio_details: list, books: list):
    # from here below still needs to be gracefully implemented

    tweets = tweet_dao.query_all()
    _details = tweet_dao._database.query(Detail).all()

    _timeline = defaultdict(list)

    min_date = datetime(year=2017, month=11, day=28)
    max_date = datetime(year=2017, month=12, day=28, hour=23, minute=59)

    _tweets = [tweet for tweet in tweets if tweet.created_at >= min_date and tweet.created_at <= max_date]
    tweet_count = len(_tweets)

    start_date = datetime(year=2017, month=11, day=28)

    while start_date < max_date:
        _timeline[transform_datetime_to_iso_date_str(start_date)] = []
        start_date += timedelta(days=1)

    twitter_words = 0

    for tweet in tweets:
        twitter_words += tweet.word_count
        _timeline[transform_datetime_to_iso_date_str(tweet.created_at)].append(tweet)

    per_day_count_by_classification = []
    for key in sorted(global_classification_model.keys()):
        per_day_count_by_classification.append({key: []})

    blog_counts_by_date = defaultdict(int)
    classification_counts = defaultdict(int)

    blog_words = 0
    total_blogs = 0

    podcast_words = 0
    total_podcasts = 0

    audio_books_words = 0
    total_audio_books = 0
    #
    # audio_book_days = defaultdict(int)
    #
    # for detail in _details:
    #     if detail.type == 'podcast':
    #         if detail.start_date >= min_date and detail.start_date <= max_date:
    #             total_podcasts += 1
    #             podcast_words += detail.word_count
    #     elif detail.type != 'blog':
    #         pass
    #
    #     key_date = transform_datetime_to_iso_date_str(detail.start_date)
    #     blog_counts_by_date[key_date] += 1
    #
    #     if detail.start_date >= min_date and detail.start_date <= max_date:
    #         total_blogs += 1
    #         blog_words += detail.word_count
    #         print(f'blog_url:{detail.url}')
    #
    # for key in sorted(_timeline.keys()):
    #     key_date = datetime.strptime(key, '%Y-%m-%d')
    #     if key_date < min_date \
    #             or key_date > max_date:
    #         continue
    #
    #     tweets = [tweet for tweet in _timeline[key]]
    #
    #     word_count = sum([tweet.word_count for tweet in tweets])
    #
    #     blogs = len([tweet.details for tweet in tweets if tweet.details and [
    #         [detail for detail in tweet.details if detail.url and detail.type == 'blog']]])
    #
    #     count = len(_timeline[key])
    #
    #     classification_values = defaultdict(int)
    #
    #     for tweet in tweets:
    #         classification_value = tweet.classification
    #
    #         if not classification_value:
    #             classification_value = 'not_classified'
    #
    #         classification_values[classification_value] += tweet.word_count
    #
    #     for audio_detail in audio_details:
    #         if key_date >= audio_detail.start_date and key_date <= audio_detail.stop_date:
    #             total_days = (audio_detail.stop_date - audio_detail.start_date).days
    #             audio_book_days[audio_detail.title] += 1
    #
    #             """
    #             https://www.quora.com/Speeches-For-the-average-person-speaking-at-a-normal-pace-what-is-the-typical-number-of-words-they-can-say-in-one-minute
    #             "publishers recommend books on tape to be voiced at 150-160 wpm"
    #             """
    #             words_per_minute = 125  # well below stated suggestion
    #             total_words = words_per_minute * audio_detail.total_audio_minutes
    #
    #             average_words_per_day = total_words / total_days
    #             audio_books_words += average_words_per_day
    #             classification_counts[audio_detail.classification] += average_words_per_day
    #             classification_values[audio_detail.classification] += average_words_per_day
    #
    #     for detail in [detail for detail in _details if detail.is_fully_classified]:
    #         if detail.start_date is not None and \
    #                         detail.stop_date is not None and \
    #                         detail.word_count is not None:
    #
    #             print(
    #                 f'type:{detail.type}, start_date:{detail.start_date.date()}, '
    #                 f'stop_date:{detail.stop_date.date()}, key_date:{key_date.date()}')
    #
    #             if (detail.start_date.date() <= key_date.date() <= detail.stop_date.date()):
    #                 total_days = (detail.stop_date - detail.start_date).days
    #                 total_days += 1
    #
    #                 word_count = detail.word_count or 0
    #                 total_words = word_count
    #
    #                 if detail.type == 'audio':
    #                     """
    #                     https://www.quora.com/Speeches-For-the-average-person-speaking-at-a-normal-pace-what-is-the-typical-number-of-words-they-can-say-in-one-minute
    #                     "publishers recommend books on tape to be voiced at 150-160 wpm"
    #                     """
    #                     words_per_minute = 10  # 125  # well below stated suggestion
    #                     total_words = words_per_minute * word_count
    #
    #                 average_words_per_day = total_words / total_days
    #                 classification_values[detail.classification] += average_words_per_day
    #
    #     display_str = ''
    #     for _key, value in classification_values.items():
    #         if display_str:
    #             display_str += ','
    #
    #         display_str += f'{_key}={value}'
    #
    #     for classification in per_day_count_by_classification:
    #         classification_name = next(iter(classification.keys()))
    #         classification_count = classification_values.get(classification_name)
    #         classification[classification_name].append(classification_count or 0)
    #
    #
    #     print(f'date={key}:tweets_count={count}:total_words={word_count}|classifications:{display_str}')
    #
    # _audio_books = []
    #
    # for audio_detail in audio_details:
    #     if not audio_detail.title in audio_book_days.keys():
    #         continue
    #
    #     days = audio_book_days[audio_detail.title]
    #
    #     total_days = (audio_detail.stop_date - audio_detail.start_date).days
    #     total_days += 1
    #
    #     book_parts = days / total_days
    #     total_audio_books += book_parts
    #     _audio_books.append((audio_detail.title, audio_detail.start_date, audio_detail.stop_date))
    #
    # print('categories =')
    # print('[')
    # for key in sorted(_timeline.keys()):
    #     if datetime.strptime(key, '%Y-%m-%d') < min_date \
    #             or datetime.strptime(key, '%Y-%m-%d') > max_date:
    #         continue
    #     blogs = blog_counts_by_date[key]
    #     print(f"'{key}',")
    # print('];')
    #
    # print('series =')
    # print('[')
    #
    #
    # for classification in per_day_count_by_classification:
    #     classification_name = next(iter(classification.keys()))
    #
    #     if sum(classification[classification_name]) == 0:
    #         continue
    #
    #     data = ''
    #     classifcation_total_words = 0
    #     for word_count in classification[classification_name]:
    #         classifcation_total_words += word_count
    #         data += f'{word_count},'
    #
    #     classification_counts[classification_name] += classifcation_total_words
    #
    #     print('{')
    #     print(f"  name: '{classification_name}',")
    #     print('  data: [')
    #     print(f'    {data}')
    #     print('        ]')
    #     print('},')
    #
    # print('];')
    #
    # print('--------------------')
    # print('--------------------')
    # print('--------------------')
    # print('--------------------')
    #
    # print('---------- table count data ----------')
    #
    # print('<div>')
    # print('  <div style="float: left;">')
    # print('    <table border="border">')
    # print('      <thead>Consumption by Type</thead>')
    # print('      <tr><th>type</th><th>count</th></tr>')
    # print(f'      <tr><td>Twitter Tweets & Favorites</td><td>{tweet_count}</td></tr>')
    # print(f'       <tr><td>Blogs</td><td>{total_blogs}</td></tr>')
    # print(f'       <tr><td>Podcasts</td><td>{total_podcasts}</td></tr>')
    # print(f'       <tr><td>Audio Books</td><td>{total_audio_books:.2f}</td></tr>')
    # print('    </table>')
    # print('  </div>')
    # print('  <div style="float: left; padding-left: 50pt">')
    # print('    <table border="border">')
    # print('      <thead>Words by Type</thead>')
    # print('      <tr><th>type</th><th>count</th></tr>')
    # print(f'      <tr><td>Twitter</td><td>{twitter_words}</td></tr>')
    # print(f'       <tr><td>Blogs</td><td>{blog_words}</td></tr>')
    # print(f'       <tr><td>Podcasts</td><td>{podcast_words}</td></tr>')
    # print(f'       <tr><td>Audio Books</td><td>{int(audio_books_words)}</td></tr>')
    # print('    </table>')
    # print('  </div>')
    # print('  <div style="float: left; padding-left: 50pt">')
    # print('    <table border="border">')
    # print('      <thead>Consumption by ''Word'' count</thead>')
    # print('      <tr><th>type</th><th>count</th></tr>')
    #
    # for classification, value in classification_counts.items():
    #     print(f'      <tr><td>{classification}</td><td>{int(value)}</td></tr>')
    #
    # print(f'      <tr><th>total</th><td>{int(sum(classification_counts.values()))}</td></tr>')
    # print('    </table>')
    # print('  </div>')
    #
    # print('  <div style="float: left; padding-left: 50pt">')
    # print('    <table border="border">')
    # print('      <thead>Audio Books</thead>')
    # print('      <tr><th>title</th><th>start</th><th>stop</th></tr>')
    #
    # for audio_book in _audio_books:
    #     print(f'      <tr><td>{audio_book[0]}</td><td>{audio_book[1].date()}</td><td>{audio_book[2].date()}</td></tr>')
    #
    # print('    </table>')
    # print('  </div>')
    #
    # print('</div>')

    return tweets
