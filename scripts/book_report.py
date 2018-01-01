from collections import defaultdict
from datetime import timedelta

from app.twitter_learning_journal.transformers.transform_datetime import transform_datetime_to_iso_date_str
from scripts.models.aggregate_result import AggregateResult


def process_books(report_start_date, report_stop_date, books):
    # assumption variables
    average_reading_speed_in_minutes = 200
    average_words_per_page = 250
    devaiation_book_pages = 50

    aggregate_result = AggregateResult('Books')

    for book in books:
        pages = book.pages - devaiation_book_pages
        word_count = pages * average_words_per_page

        days_to_read_book = (book.stop_date - book.start_date).days + 1

        total_minutes = word_count / average_reading_speed_in_minutes
        total_hours = total_minutes / 60

        average_knowlege_consumption_velocity = total_hours / days_to_read_book

        days_overlap = 0
        date_list = [book.stop_date - timedelta(days=day) for day in range(0, days_to_read_book)]

        for book_date in date_list:
            book_date_key = transform_datetime_to_iso_date_str(book_date)
            if book_date >= report_start_date and book_date <= report_stop_date:
                if book_date_key not in aggregate_result.timeline:
                    aggregate_result.timeline[book_date_key] = defaultdict(int)

                aggregate_result.timeline[book_date_key][book.classification] += average_knowlege_consumption_velocity
                # words = average_knowlege_consumption_velocity * 60 * average_reading_speed_in_minutes
                # aggregate_result.timeline[book_date_key][book.classification] += int(words)
                days_overlap += 1

        distribution_percent = days_overlap / days_to_read_book

        aggregate_result.item_count += distribution_percent
        aggregate_result.kcv += average_knowlege_consumption_velocity * days_overlap

        book_report = create_book_report(book, distribution_percent)
        aggregate_result.book_reports.append(book_report)

    aggregate_result.book_reports.sort(key=lambda book_report: book_report.start_date, reverse=True)

    return aggregate_result


def process_audio_books(report_start_date, report_stop_date, audio_books):
    aggregate_result = AggregateResult('Audio Books')

    for audio_book in audio_books:
        days_to_hear_book = (audio_book.stop_date - audio_book.start_date).days + 1
        total_hours = audio_book.length / 60

        average_knowlege_consumption_velocity = total_hours / days_to_hear_book

        days_overlap = 0
        date_list = [audio_book.stop_date - timedelta(days=day) for day in range(0, days_to_hear_book)]

        for book_date in date_list:
            book_date_key = transform_datetime_to_iso_date_str(book_date)
            if book_date >= report_start_date and book_date <= report_stop_date:
                if book_date_key not in aggregate_result.timeline:
                    aggregate_result.timeline[book_date_key] = defaultdict(int)

                aggregate_result.timeline[book_date_key][
                    audio_book.classification] += average_knowlege_consumption_velocity
                # words = average_knowlege_consumption_velocity * 60 * 150 # 150 spoken words / minute
                # aggregate_result.timeline[book_date_key][audio_book.classification] += int(words)

                days_overlap += 1

        distribution_percent = days_overlap / days_to_hear_book

        aggregate_result.item_count += distribution_percent
        aggregate_result.kcv += average_knowlege_consumption_velocity * days_overlap

        audio_book_report = create_book_report(audio_book, distribution_percent, is_book=False)
        aggregate_result.book_reports.append(audio_book_report)

    aggregate_result.book_reports.sort(key=lambda book_report: book_report.start_date, reverse=True)

    return aggregate_result


def create_book_report(book, distribution_percent, *, is_book=True):
    from server import BookReport
    book_report = BookReport()

    title = book.title.title()
    if 'Pm' in title:
        title = title.replace('Pm', 'PM')
    if 'F*Cked' in title:
        title = title.replace('F*Cked', 'F*cked')

    book_report.title = title
    book_report.classification = book.classification
    book_report.start_date = book.start_date.date()
    book_report.stop_date = book.stop_date.date()

    if is_book:
        book_report.length = f'{book.pages} pages'
    else:
        book_report.medium = 'Audio Book'
        book_report.length = f'{int(book.length)} minutes'
        pass

    book_report.distribution_percent = f'{distribution_percent:.2f}'

    return book_report
