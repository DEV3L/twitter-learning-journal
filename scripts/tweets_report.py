from collections import defaultdict

from app.twitter_learning_journal.transformers.transform_datetime import transform_datetime_to_iso_date_str
from scripts import average_tweet_reading_speed
from scripts.models.aggregate_result import AggregateResult
from scripts.models.report_entry import ReportEntry


def process_tweets(tweets):
    aggregate_result = AggregateResult('Tweets')

    for tweet in tweets:
        words = tweet.word_count
        tweet_date_key = transform_datetime_to_iso_date_str(tweet.created_at)
        minutes = words / average_tweet_reading_speed
        hours = minutes / 60

        if tweet_date_key not in aggregate_result.timeline:
            aggregate_result.timeline[tweet_date_key] = defaultdict(int)

        aggregate_result.timeline[tweet_date_key][tweet.classification] += hours
        aggregate_result.item_count += 1
        aggregate_result.kcv += hours

        tweet_report_entry = create_tweet_report_entry(tweet, minutes)
        aggregate_result.report_entries.append(tweet_report_entry)

    aggregate_result.report_entries.sort(key=lambda tweet_report_entry: tweet_report_entry.start_date, reverse=True)

    return aggregate_result


def create_tweet_report_entry(tweet, minutes):
    report_entry = ReportEntry()

    title = tweet.full_text
    title = title.replace('\n', '')
    title = ' '.join(title.split())

    if len(title) > 50:
        title = title[:50]

    report_entry.title = title
    report_entry.url = tweet.full_text
    report_entry.classification = tweet.classification
    report_entry.start_date = tweet.created_at.date()
    report_entry.stop_date = tweet.created_at.date()
    report_entry.length = f'{minutes:.2f} minutes'
    report_entry.distribution_percent = 1

    return report_entry
