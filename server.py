import traceback
from collections import defaultdict
from datetime import datetime

from flask import Flask, render_template, request
from flask_script import Manager

from app.twitter_learning_journal.dao.tweet_dao import TweetDao
from app.twitter_learning_journal.database.sqlalchemy_database import Database
from scripts.audio_books import get_audio_books
from scripts.book_report import process_books, process_audio_books
from scripts.books import get_books
from scripts.timeline import build_timeline, _create_per_day_count_by_classification

app = Flask(__name__)
manager = Manager(app)

default_screen_name = 'dev3l_'
default_report_start_date = '2017-11-28'
default_report_stop_date = '2017-12-28'

@app.route("/")
def index():
    try:
        return _index()
    except Exception as e:
        print(e)
        traceback.print_exc()


def _index():
    aggregates = []
    aggregate_timelines = []
    book_reports = []

    tweet_dao = TweetDao(Database())

    screen_name = request.args.get('screen_name', default_screen_name)
    report_start_date, report_stop_date = get_report_date_ranges(request.args.get('report_start_date'),
                                                                 request.args.get('report_stop_date'))

    timeline = build_timeline(report_start_date, report_stop_date)

    per_day_count_by_classification = _create_per_day_count_by_classification()

    # books
    books = [book for book in get_books()]
    filtered_books = [book for book in books
                      if book.start_date <= report_stop_date and book.stop_date >= report_start_date]
    books_aggregate_result = process_books(report_start_date, report_stop_date, filtered_books)
    aggregates.append(books_aggregate_result)
    aggregate_timelines.append(books_aggregate_result.timeline)
    book_reports.extend(books_aggregate_result.book_reports)

    # audio books
    audio_books = get_audio_books()
    filtered_audio_books = [audio_book for audio_book in audio_books
                            if audio_book.start_date <= report_stop_date and audio_book.stop_date >= report_start_date]
    audio_books_aggregate_result = process_audio_books(report_start_date, report_stop_date, filtered_audio_books)
    aggregates.append(audio_books_aggregate_result)
    aggregate_timelines.append(audio_books_aggregate_result.timeline)
    book_reports.extend(audio_books_aggregate_result.book_reports)


    # tweets = tweet_dao.query_all()
    # filtered_tweets = [tweet for tweet in tweets
    #                    if tweet.created_at >= report_start_date and tweet.created_at <= report_stop_date]
    #
    # details = tweet_dao._database.query(Detail).all()
    # filtered_details = [detail for detail in details
    #                     if detail.start_date >= report_start_date and detail.stop_date <= report_stop_date]


    # timeline = create_timeline(report_start_date, report_stop_date,
    #                            filtered_tweets, filtered_details,
    #                            filtered_audio_books, filtered_books)

    # aggregates
    results = []

    for aggregate in aggregates:
        results.append(
            (aggregate.medium,
             f'{aggregate.item_count:.2f}',
             0,
             f'{aggregate.kcv:.2f}')
        )

    results.extend([
        ('Podcasts', 19, 111479, 0),
        ('Blogs', 123, 219572, 0),
        ('Tweets & Favorites', 319, 36474, 0),
        # ('TOTAL', '-', 429391, 0),
    ])

    # timelines
    for aggregate_timeline in aggregate_timelines:
        for key_date, aggregate_timeline_entry in aggregate_timeline.items():
            timeline_entry = timeline[key_date]

            for timeline_entry_classification in timeline_entry.keys():
                timeline_entry[timeline_entry_classification] += aggregate_timeline_entry[timeline_entry_classification]

    def transform_timeline_into_series(timeline):
        series = defaultdict(list)

        for key_date, daily_classifications in timeline.items():
            for classification in daily_classifications:
                series[classification].append(daily_classifications[classification])

        return series

    _series = transform_timeline_into_series(timeline)

    series = []

    for classification, data in _series.items():
        node = {}
        node['name'] = classification
        node['data'] = data
        series.append(node)

    series.sort(key=lambda node: node['name'])

    categories = [key for key in timeline.keys()]

    return render_template('report.jinja',
                           name=None,
                           series=series,
                           categories=categories,
                           results=results,
                           book_reports=book_reports)

def get_report_date_ranges(report_start_date_str, report_stop_date_str):
    report_start_date_str = report_start_date_str or default_report_start_date
    report_stop_date_str = report_stop_date_str or default_report_stop_date

    report_start_date_str_parts = [int(date_part) for date_part in (report_start_date_str).split('-')]
    report_stop_date_str_parts = [int(date_part) for date_part in report_stop_date_str.split('-')]

    report_start_date = datetime(year=report_start_date_str_parts[0],
                                 month=report_start_date_str_parts[1],
                                 day=report_start_date_str_parts[2])
    report_stop_date = datetime(year=report_stop_date_str_parts[0],
                                month=report_stop_date_str_parts[1],
                                day=report_stop_date_str_parts[2],
                                hour=23, minute=59, second=59)

    return report_start_date, report_stop_date


class BookReport:
    def __init__(self):
        self.medium = 'Book'

        self.title = None
        self.classification = None

        self.length = 0

        self.start_date = None
        self.stop_date = None

        self.distribution_percent = None


if __name__ == "__main__":
    manager.run()
