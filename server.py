import traceback
from collections import defaultdict
from datetime import datetime

from flask import Flask, render_template, request
from flask_script import Manager

from app.twitter_learning_journal.dao.tweet_dao import TweetDao
from app.twitter_learning_journal.database.sqlalchemy_database import Database
from scripts.audio_books import get_audio_books
from scripts.book_report import process_books
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

    audio_books = get_audio_books()
    filtered_audio_books = [audio_book for audio_book in audio_books
                            if audio_book.start_date <= report_stop_date and audio_book.stop_date <= report_start_date]

    # books
    books = [book for book in get_books()]
    filtered_books = [book for book in books
                      if book.start_date <= report_stop_date and book.stop_date >= report_start_date]
    books_aggregate_result = process_books(report_start_date, report_stop_date, filtered_books)
    aggregates.append(books_aggregate_result)
    aggregate_timelines.append(books_aggregate_result.timeline)

    book_reports.extend(books_aggregate_result.book_reports)



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
        # ('Books', 0, 0, 0),
        ('Audio Books', 1.86, 101250, 0),
        ('Podcasts', 19, 111479, 0),
        ('Blogs', 123, 219572, 0),
        ('Tweets & Favorites', 319, 36474, 0),
        ('TOTAL', '-', 429391, 0),
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

    series = [
        {
            'name': 'agile',
            'data': [
                2201.0, 3213.0, 2058.0, 973.0, 1534.0, 4223.0, 8696.0, 5336.0, 14535.0, 5415.0, 7246.0, 3798.0, 1664.0,
                16595.0, 9306.0, 7880.0, 9082.0, 7846.0, 8858.0, 3686.0, 16611.0, 8115.0, 0, 111, 256, 12969.0, 146, 93,
                9268.0, 8755.0, 31080.0,
            ]
        },
        {
            'name': 'engineering',
            'data': [
                7784.0, 4039.0, 22, 233, 4143.0, 2357.0, 5403.0, 3484.0, 36, 989.0, 10, 2730.0, 20, 46, 0, 800.0, 16,
                106, 39, 6626.0, 0, 2824.0, 31, 50, 1509.0, 78, 947.0, 554.0, 33, 4061.0, 0,
            ]
        },
        {
            'name': 'leadership',
            'data': [
                10433.0, 9173.0, 9125.0, 9172.0, 9125.0, 9687.0, 1304.0, 41, 0, 1276.0, 873.0, 561.0, 1642.0, 0, 735.0,
                0, 0, 541.0, 16, 1389.0, 0, 1435.0, 40, 0, 541.0, 0, 0, 0, 105, 408.0, 0,
            ]
        },
    ]

    for entry in series:
        classification = entry['name']
        entry_data = entry['data']

        timeline_data = _series[classification]

        for index, data_point in enumerate(timeline_data):
            entry_data[index] += data_point

    # end timelines

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
