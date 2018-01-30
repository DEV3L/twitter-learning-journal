from collections import defaultdict

from app.twitter_learning_journal.transformers.transform_datetime import transform_datetime_to_iso_date_str
from scripts.models.aggregate_result import AggregateResult
from scripts.models.report_entry import ReportEntry


def process_podcasts(podcasts):
    aggregate_result = AggregateResult('Podcasts')

    for podcast in podcasts:
        minutes = podcast.count
        hours = minutes / 60

        podcast_date_key = transform_datetime_to_iso_date_str(podcast.tweet.created_at)

        if podcast_date_key not in aggregate_result.timeline:
            aggregate_result.timeline[podcast_date_key] = defaultdict(int)

        aggregate_result.timeline[podcast_date_key][podcast.classification] += hours
        aggregate_result.item_count += 1
        aggregate_result.kcv += hours

        podcast_report_entry = create_podcast_report_entry(podcast, minutes)
        aggregate_result.report_entries.append(podcast_report_entry)

    aggregate_result.report_entries.sort(key=lambda podcast_report_entry: podcast_report_entry.start_date, reverse=True)

    return aggregate_result


def create_podcast_report_entry(podcast, minutes):
    report_entry = ReportEntry()

    title = podcast.title.title()

    report_entry.title = title
    report_entry.classification = podcast.classification
    report_entry.start_date = podcast.tweet.created_at.date()
    report_entry.stop_date = podcast.tweet.created_at.date()
    report_entry.length = f'{int(minutes)} minutes'
    report_entry.distribution_percent = 1

    return report_entry
