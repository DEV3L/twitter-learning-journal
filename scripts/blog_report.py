from collections import defaultdict

from app.twitter_learning_journal.transformers.transform_datetime import transform_datetime_to_iso_date_str
from scripts import average_blog_reading_speed
from scripts.models.aggregate_result import AggregateResult
from scripts.models.report_entry import ReportEntry


def process_blogs(blogs):
    aggregate_result = AggregateResult('Blogs')

    for blog in blogs:
        words = blog.word_count
        blog_date_key = transform_datetime_to_iso_date_str(blog.start_date)
        minutes = words / average_blog_reading_speed
        hours = minutes / 60

        if blog_date_key not in aggregate_result.timeline:
            aggregate_result.timeline[blog_date_key] = defaultdict(int)

        aggregate_result.timeline[blog_date_key][blog.classification] += hours
        aggregate_result.item_count += 1
        aggregate_result.kcv += hours

        blog_report_entry = create_blog_report_entry(blog, minutes)
        aggregate_result.report_entries.append(blog_report_entry)

    aggregate_result.report_entries.sort(key=lambda blog_report_entry: blog_report_entry.start_date, reverse=True)

    return aggregate_result


def create_blog_report_entry(blog, minutes):
    report_entry = ReportEntry()

    title = blog.title
    title = title.replace('http://', '')
    title = title.replace('https://', '')
    title = title.replace('www.', '')
    title = title.replace('.com', '')
    title = title.replace('.org', '')

    if '?' in title:
        title = title[:title.find('?')]

    title = title.replace('/', ' ')
    if len(title) > 75:
        title = title[:75]

    title = title.title()

    report_entry.title = title
    report_entry.url = blog.title
    report_entry.classification = blog.classification
    report_entry.start_date = blog.start_date.date()
    report_entry.stop_date = blog.stop_date.date()
    report_entry.length = f'{minutes:.2f} minutes'
    report_entry.distribution_percent = 1

    return report_entry
