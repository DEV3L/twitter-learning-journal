from collections import defaultdict

from app.twitter_learning_journal.transformers.transform_datetime import transform_datetime_to_iso_date_str
from scripts.models.aggregate_result import AggregateResult
from scripts.models.report_entry import ReportEntry
from scripts.podcasts import podcast_words_per_minute


def process_podcasts(podcasts):
    aggregate_result = AggregateResult('Podcasts')

    for podcast in podcasts:
        words = podcast.word_count
        minutes = words / podcast_words_per_minute
        hours = minutes / 60

        podcast_date_key = transform_datetime_to_iso_date_str(podcast.start_date)

        if podcast_date_key not in aggregate_result.timeline:
            aggregate_result.timeline[podcast_date_key] = defaultdict(int)

        aggregate_result.timeline[podcast_date_key][podcast.classification] += hours
        aggregate_result.item_count += 1
        aggregate_result.kcv += hours

        podcast_report = create_podcast_report_entry(podcast, minutes)
        aggregate_result.report_entries.append(podcast_report)

    aggregate_result.report_entries.sort(key=lambda book_report: book_report.start_date, reverse=True)

    return aggregate_result


def create_podcast_report_entry(podcast, minutes):
    report_entry = ReportEntry()

    title = podcast.title.title()

    report_entry.title = title
    report_entry.classification = podcast.classification
    report_entry.start_date = podcast.start_date.date()
    report_entry.stop_date = podcast.stop_date.date()
    report_entry.length = f'{minutes} minutes'
    report_entry.distribution_percent = 1

    return report_entry
