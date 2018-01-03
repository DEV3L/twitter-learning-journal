import traceback
from collections import defaultdict
from datetime import datetime

from flask import Flask, render_template, request
from flask_script import Manager

from app.twitter_learning_journal.dao.tweet_dao import TweetDao
from app.twitter_learning_journal.database.sqlalchemy_database import Database
from app.twitter_learning_journal.models.detail import Detail
from scripts.audio_books import get_audio_books
from scripts.blog_report import process_blogs
from scripts.book_report import process_books, process_audio_books
from scripts.books import get_books
from scripts.github_report import process_github
from scripts.podcast_report import process_podcasts
from scripts.timeline import build_timeline
from scripts.tweets_report import process_tweets

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

    book_entry_reports = []
    podcast_entry_reports = []
    blogs_entry_reports = []
    tweet_entry_reports = []
    github_entry_reports = []

    database = Database()
    tweet_dao = TweetDao(database)

    tweets = tweet_dao.query_all()
    details = database.query(Detail).all()

    screen_name = request.args.get('screen_name', default_screen_name)

    report_start_date, report_stop_date = get_report_date_ranges(request.args.get('report_start_date'),
                                                                 request.args.get('report_stop_date'))

    filtered_tweets = [tweet for tweet in tweets
                       if report_start_date <= tweet.created_at <= report_stop_date]

    filtered_details = [detail for detail in details
                        if report_stop_date >= detail.start_date >= report_start_date]

    timeline = build_timeline(report_start_date, report_stop_date)


    # books
    books = [book for book in get_books()]
    filtered_books = [book for book in books
                      if book.start_date <= report_stop_date and book.stop_date >= report_start_date]
    books_aggregate_result = process_books(report_start_date, report_stop_date, filtered_books)
    aggregates.append(books_aggregate_result)
    aggregate_timelines.append(books_aggregate_result.timeline)
    book_entry_reports.extend(books_aggregate_result.report_entries)

    # audio books
    audio_books = get_audio_books()
    filtered_audio_books = [audio_book for audio_book in audio_books
                            if audio_book.start_date <= report_stop_date and audio_book.stop_date >= report_start_date]
    audio_books_aggregate_result = process_audio_books(report_start_date, report_stop_date, filtered_audio_books)
    aggregates.append(audio_books_aggregate_result)
    aggregate_timelines.append(audio_books_aggregate_result.timeline)
    book_entry_reports.extend(audio_books_aggregate_result.report_entries)

    # podcasts
    podcast_details = [detail for detail in filtered_details if detail.type == 'podcast']
    podcast_aggregate_result = process_podcasts(podcast_details)
    aggregates.append(podcast_aggregate_result)
    aggregate_timelines.append(podcast_aggregate_result.timeline)
    podcast_entry_reports.extend(podcast_aggregate_result.report_entries)

    # blogs
    blog_details = [detail for detail in filtered_details if detail.type == 'blog']
    blog_aggregate_result = process_blogs(blog_details)
    aggregates.append(blog_aggregate_result)
    aggregate_timelines.append(blog_aggregate_result.timeline)
    blogs_entry_reports.extend(blog_aggregate_result.report_entries)

    # tweets
    tweet_aggregate_result = process_tweets(filtered_tweets)
    aggregates.append(tweet_aggregate_result)
    aggregate_timelines.append(tweet_aggregate_result.timeline)
    tweet_entry_reports.extend(tweet_aggregate_result.report_entries)

    # github
    github_aggregate_result = process_github(report_start_date, report_stop_date)
    aggregates.append(github_aggregate_result)
    aggregate_timelines.append(github_aggregate_result.timeline)
    github_entry_reports.extend(github_aggregate_result.report_entries)

    # aggregates
    results = []

    total_kcv = 0

    for aggregate in aggregates:
        total_kcv += aggregate.kcv

        item_count_int = int(aggregate.item_count)
        _item_count = item_count_int if item_count_int == aggregate.item_count else f'{aggregate.item_count:.2f}'

        results.append(
            (aggregate.medium,
             _item_count,
             f'{aggregate.kcv:.2f}')
        )

    report_period_day_count = (report_stop_date - report_start_date).days + 1
    average_kcv = total_kcv / report_period_day_count

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
                series[classification].append(f'{daily_classifications[classification]:.2f}')

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
                           book_entry_reports=book_entry_reports,
                           blog_entry_reports=blogs_entry_reports,
                           podcast_entry_reports=podcast_entry_reports,
                           tweet_entry_reports=tweet_entry_reports,
                           tkcv=f'{total_kcv:.2f} hours',
                           akcv=f'{average_kcv:.2f} hours/day', )

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




if __name__ == "__main__":
    manager.run()
