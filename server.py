from datetime import datetime, timedelta

from flask import Flask, render_template, request
from flask_script import Manager

from app.twitter_learning_journal.dao.tweet_dao import TweetDao
from app.twitter_learning_journal.database.sqlalchemy_database import Database
from app.twitter_learning_journal.transformers.transform_datetime import transform_datetime_to_iso_date_str
from scripts.audio_books import get_audio_books
from scripts.books import get_books
from scripts.timeline import build_timeline, _create_per_day_count_by_classification

app = Flask(__name__)
manager = Manager(app)

default_screen_name = 'dev3l_'
default_report_start_date = '2017-11-28'
default_report_stop_date = '2017-12-28'


class AggregateResult:
    type = None
    item_count = None
    word_count = None
    kcv = None


def _process_books(report_start_date, report_stop_date, books, timeline):
    for book in books:
        average_reading_speed_in_minutes = 200
        average_words_per_page = 275
        devaiation_book_pages = 50

        pages = book.pages - devaiation_book_pages
        word_count = pages * average_words_per_page

        days_to_read_book = (book.stop_date - book.start_date).days + 1

        total_minutes = word_count * average_reading_speed_in_minutes
        total_hours = total_minutes / 60

        average_knowlege_consumption_velocity = total_hours / days_to_read_book

        days_overlap = 0
        date_list = [book.stop_date - timedelta(days=day) for day in range(0, days_to_read_book)]

        for book_date in date_list:
            book_date_key = transform_datetime_to_iso_date_str(book_date)
            if book_date >= report_start_date and book_date <= report_stop_date:
                # timeline[book_date_key] += average_knowlege_consumption_velocity
                # days_overlap += 1
                pass

        # timeline
        """
        aKCV = hours_per_day
        aKCV = 0.4797 hours/day

        tKCV = hours_per_day x days_overlap
        tKCV = 0.4797 hours/day x 13 days
        tKCV = 6.2361 hours / report period

        """

        pass

    pass


@app.route("/")
def index():
    tweet_dao = TweetDao(Database())

    screen_name = request.args.get('screen_name', default_screen_name)
    report_start_date, report_stop_date = get_report_date_ranges(request.args.get('report_start_date'),
                                                                 request.args.get('report_stop_date'))

    timeline = build_timeline(report_start_date, report_stop_date)
    per_day_count_by_classification = _create_per_day_count_by_classification()

    audio_books = get_audio_books()
    filtered_audio_books = [audio_book for audio_book in audio_books
                            if audio_book.start_date <= report_stop_date and audio_book.stop_date <= report_start_date]

    books = [book for book in get_books()]
    filtered_books = [book for book in books
                      if book.start_date <= report_stop_date and book.stop_date >= report_start_date]

    # _process_books(report_start_date, report_stop_date, filtered_books, timeline)

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

    results = [
        ('Books', 0, 0, 0),
        ('Audio Books', 1.86, 101250, 0),
        ('Podcasts', 19, 111479, 0),
        ('Blogs', 123, 219572, 0),
        ('Tweets & Favorites', 319, 36474, 0),
        ('TOTAL', '-', 429391, 0),
    ]

    # categories = [].extend(timeline.keys())

    categories = """
    [
        '2017-11-28',
        '2017-11-29',
        '2017-11-30',
        '2017-12-01',
        '2017-12-02',
        '2017-12-03',
        '2017-12-04',
        '2017-12-05',
        '2017-12-06',
        '2017-12-07',
        '2017-12-08',
        '2017-12-09',
        '2017-12-10',
        '2017-12-11',
        '2017-12-12',
        '2017-12-13',
        '2017-12-14',
        '2017-12-15',
        '2017-12-16',
        '2017-12-17',
        '2017-12-18',
        '2017-12-19',
        '2017-12-20',
        '2017-12-21',
        '2017-12-22',
        '2017-12-23',
        '2017-12-24',
        '2017-12-25',
        '2017-12-26',
        '2017-12-27',
        '2017-12-28',
    ];
    """
    series = """
    [
        {
            name: 'agile',
            data: [
                2201.0, 3213.0, 2058.0, 973.0, 1534.0, 4223.0, 8696.0, 5336.0, 14535.0, 5415.0, 7246.0, 3798.0, 1664.0,
                16595.0, 9306.0, 7880.0, 9082.0, 7846.0, 8858.0, 3686.0, 16611.0, 8115.0, 0, 111, 256, 12969.0, 146, 93,
                9268.0, 8755.0, 31080.0,
            ]
        },
        {
            name: 'engineering',
            data: [
                7784.0, 4039.0, 22, 233, 4143.0, 2357.0, 5403.0, 3484.0, 36, 989.0, 10, 2730.0, 20, 46, 0, 800.0, 16,
                106, 39, 6626.0, 0, 2824.0, 31, 50, 1509.0, 78, 947.0, 554.0, 33, 4061.0, 0,
            ]
        },
        {
            name: 'leadership',
            data: [
                10433.0, 9173.0, 9125.0, 9172.0, 9125.0, 9687.0, 1304.0, 41, 0, 1276.0, 873.0, 561.0, 1642.0, 0, 735.0,
                0, 0, 541.0, 16, 1389.0, 0, 1435.0, 40, 0, 541.0, 0, 0, 0, 105, 408.0, 0,
            ]
        },
    ];
    """

    return render_template('report.jinja', name=None, series=series, categories=categories, results=results)


def get_report_date_ranges(report_start_date_str, report_stop_date_str):
    report_start_date_str = report_start_date_str or default_report_start_date
    report_stop_date_str = report_stop_date_str or default_report_start_date

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


if __name__ == "__main__":
    manager.run()
