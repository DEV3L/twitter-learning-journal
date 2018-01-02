from scripts.models.aggregate_result import AggregateResult
from scripts.models.report_entry import ReportEntry


def process_tweets(tweets):
    aggregate_result = AggregateResult('Tweets')

    return
    #
    # for tweet in tweets:
    #     words = tweet.word_count
    #     blog_date_key = transform_datetime_to_iso_date_str(tweet.created_at)
    #     minutes = words / average_tweet_reading_speed
    #     hours = minutes / 60
    #
    #     if blog_date_key not in aggregate_result.timeline:
    #         aggregate_result.timeline[blog_date_key] = defaultdict(int)
    #
    #     aggregate_result.timeline[blog_date_key][tweet.classification] += hours
    #     aggregate_result.item_count += 1
    #     aggregate_result.kcv += hours
    #
    #     podcast_report = create_blog_report_entry(tweet, minutes)
    #     aggregate_result.report_entries.append(podcast_report)
    #
    # aggregate_result.report_entries.sort(key=lambda book_report: book_report.start_date, reverse=True)
    #
    # return aggregate_result


def create_blog_report_entry(tweet, minutes):
    report_entry = ReportEntry()

    title = tweet.title
    title = title.replace('\n', '')
    title = ' '.join(title.split())

    if len(title) > 50:
        title = title[:50]

    report_entry.title = title
    report_entry.url = tweet.title
    report_entry.classification = tweet.classification
    report_entry.start_date = tweet.start_date.date()
    report_entry.stop_date = tweet.stop_date.date()
    report_entry.length = f'{minutes:.2f} minutes'
    report_entry.distribution_percent = 1

    return report_entry
