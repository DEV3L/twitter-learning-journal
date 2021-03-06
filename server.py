import traceback
from collections import defaultdict
from datetime import datetime

from flask import Flask, render_template, request
from flask_script import Manager

from app.twitter_learning_journal.controllers.dashboard import dashboard_blueprint
from app.twitter_learning_journal.controllers.login import login_blueprint
from app.twitter_learning_journal.dao.tweet_dao import TweetDao
from app.twitter_learning_journal.database.sqlalchemy_database import Database
from app.twitter_learning_journal.models.detail import Detail
from app.twitter_learning_journal.retrievers.details.books import get_books
from app.twitter_learning_journal.retrievers.details.conferences import get_conferences
from app.twitter_learning_journal.retrievers.details.pairings import get_pairings
from app.twitter_learning_journal.retrievers.details.videos import get_videos
from scripts.audio_books import get_audio_books
from scripts.blog_report import process_blogs
from scripts.book_report import process_books, process_audio_books, process_videos, process_pairings, \
    process_conferences
from scripts.github_report import process_github
from scripts.podcast_report import process_podcasts
from scripts.timeline import build_timeline
from scripts.tweets_report import process_tweets

app = Flask(__name__)
app.register_blueprint(dashboard_blueprint)
app.register_blueprint(login_blueprint)

manager = Manager(app)

default_screen_name = 'dev3l_'
default_report_start_date = '2017-04-10'
default_report_stop_date = '2018-07-27'


@app.route("/", methods=['GET', 'POST'])
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
    video_entry_reports = []
    pairing_entry_reports = []
    conference_entry_reports = []

    database = Database()
    tweet_dao = TweetDao(database)

    tweets = tweet_dao.query_all()
    details = database.query(Detail).all()

    screen_name = request.args.get('screen_name', default_screen_name)

    report_start_date, report_stop_date = get_report_date_ranges(
        request.args.get('report_start_date') or request.form.get('report_start_date'),
        request.args.get('report_stop_date') or request.form.get('report_stop_date'), )

    filtered_tweets = [tweet for tweet in tweets
                       if report_start_date <= tweet.created_at <= report_stop_date
                       # and tweet.classification == 'agile'
                       ]

    filtered_details = [detail for detail in details
                        if report_stop_date >= detail.tweet.created_at >= report_start_date]

    timeline = build_timeline(report_start_date, report_stop_date)

    # books
    books = get_books(tweets)
    filtered_books = [book for book in books
                      if book.start_date <= report_stop_date
                      and book.stop_date >= report_start_date
                      # and book.classification == 'agile'
                      ]
    books_aggregate_result = process_books(report_start_date, report_stop_date, filtered_books)
    aggregates.append(books_aggregate_result)
    aggregate_timelines.append(books_aggregate_result.timeline)
    book_entry_reports.extend(books_aggregate_result.report_entries)

    # audio books
    audio_books = get_audio_books()
    filtered_audio_books = [audio_book for audio_book in audio_books
                            if audio_book.start_date <= report_stop_date
                            and audio_book.stop_date >= report_start_date
                            # and audio_book.classification == 'agile'
                            ]
    audio_books_aggregate_result = process_audio_books(report_start_date, report_stop_date, filtered_audio_books)
    aggregates.append(audio_books_aggregate_result)
    aggregate_timelines.append(audio_books_aggregate_result.timeline)
    book_entry_reports.extend(audio_books_aggregate_result.report_entries)

    # podcasts
    podcast_details = [detail for detail in filtered_details
                       if detail.type == 'podcast'
                       # and detail.classification == 'agile'
                       ]
    podcast_aggregate_result = process_podcasts(podcast_details)
    aggregates.append(podcast_aggregate_result)
    aggregate_timelines.append(podcast_aggregate_result.timeline)
    podcast_entry_reports.extend(podcast_aggregate_result.report_entries)

    # blogs
    blog_details = [detail for detail in filtered_details
                    if detail.type == 'blog'
                    # and detail.classification == 'agile'
    ]
    blog_aggregate_result = process_blogs(blog_details)
    aggregates.append(blog_aggregate_result)
    aggregate_timelines.append(blog_aggregate_result.timeline)
    blogs_entry_reports.extend(blog_aggregate_result.report_entries)

    # tweets
    tweet_aggregate_result = process_tweets(filtered_tweets)
    aggregates.append(tweet_aggregate_result)
    aggregate_timelines.append(tweet_aggregate_result.timeline)
    tweet_entry_reports.extend(tweet_aggregate_result.report_entries)

    # videos
    videos = get_videos([tweet for tweet in tweets
                         # if tweet.classification == 'agile'
                         ])
    filtered_videos = [video for video in videos
                       if video.created_at <= report_stop_date and video.created_at >= report_start_date]
    videos_aggregate_result = process_videos(filtered_videos)
    aggregates.append(videos_aggregate_result)
    aggregate_timelines.append(videos_aggregate_result.timeline)
    video_entry_reports.extend(videos_aggregate_result.report_entries)

    # conferences
    conferences = get_conferences([tweet for tweet in tweets
                                   # if tweet.classification == 'agile'
                                   ])
    filtered_conferences = [conference for conference in conferences
                       if conference.created_at <= report_stop_date and conference.created_at >= report_start_date]
    conferences_aggregate_result = process_conferences(filtered_conferences)
    aggregates.append(conferences_aggregate_result)
    aggregate_timelines.append(conferences_aggregate_result.timeline)
    conference_entry_reports.extend(conferences_aggregate_result.report_entries)

    # engineering
    # github
    github_aggregate_result = process_github(report_start_date, report_stop_date)
    aggregates.append(github_aggregate_result)
    aggregate_timelines.append(github_aggregate_result.timeline)
    github_entry_reports.extend(github_aggregate_result.report_entries)

    # pairing
    pairings = get_pairings(tweets)
    filtered_pairings = [pairing for pairing in pairings
                       if pairing.created_at <= report_stop_date and pairing.created_at >= report_start_date]
    pairings_aggregate_result = process_pairings(filtered_pairings)
    aggregates.append(pairings_aggregate_result)
    aggregate_timelines.append(pairings_aggregate_result.timeline)
    pairing_entry_reports.extend(pairings_aggregate_result.report_entries)

    # aggregates
    results = []

    total_kcv = 0

    mediums = {
        'Books': 'books',
        'Audio Books': 'books',
        'GitHub': 'commits',
        'Podcasts': 'podcasts',
        'Blogs': 'blogs',
        'Tweets': 'tweets/favorites',
        'Videos': 'videos',
        'Pairing': 'pairing',
        'Conferences': 'conferences'
    }

    for aggregate in aggregates:
        total_kcv += aggregate.kcv

        item_count_int = int(aggregate.item_count)
        _item_count = item_count_int if item_count_int == aggregate.item_count else f'{aggregate.item_count:.2f}'

        _item_count = f'{_item_count} {mediums[aggregate.medium]}'

        results.append(
            (aggregate.medium,
             _item_count,
             f'{aggregate.kcv:.2f} hours')
        )

    report_period_day_count = (report_stop_date - report_start_date).days + 1
    average_kcv = total_kcv / report_period_day_count

    # timelines
    for aggregate_timeline in aggregate_timelines:
        for key_date, aggregate_timeline_entry in aggregate_timeline.items():
            timeline_entry = timeline[key_date]

            for timeline_entry_classification in timeline_entry.keys():
                timeline_entry[timeline_entry_classification] += aggregate_timeline_entry[timeline_entry_classification]

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
                           github_entry_reports=github_entry_reports,
                           video_entry_reports=video_entry_reports,
                           pairing_entry_reports=pairing_entry_reports,
                           conference_entry_reports=conference_entry_reports,
                           tkcv=f'{total_kcv:.2f} total hours',
                           akcv=f'{average_kcv:.2f} hours/day',
                           report_start_date=report_start_date.date(),
                           report_stop_date=report_stop_date.date())

def transform_timeline_into_series(timeline):
    series = defaultdict(list)

    for key_date, daily_classifications in timeline.items():
        for classification in daily_classifications:
            # if classification != "agile":
            #     continue
            series[classification].append(f'{daily_classifications[classification]:.2f}')

    return series

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
    # app.register_blueprint(blueprint)

    manager.run()
