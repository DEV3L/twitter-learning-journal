from collections import defaultdict
from datetime import timedelta

from app.twitter_learning_journal.transformers.transform_datetime import transform_datetime_to_iso_date_str
from scripts import average_reading_speed_in_minutes, average_words_per_page, devaiation_book_pages
from scripts.models.aggregate_result import AggregateResult
from scripts.models.report_entry import ReportEntry


def process_books(report_start_date, report_stop_date, books):
    aggregate_result = AggregateResult('Books')

    for book in books:
        pages = book.pages - devaiation_book_pages
        count = pages * average_words_per_page

        days_to_read_book = (book.stop_date - book.start_date).days + 1

        total_minutes = count / average_reading_speed_in_minutes
        total_hours = total_minutes / 60

        average_knowlege_consumption_velocity = total_hours / days_to_read_book

        days_overlap = 0
        date_list = [book.stop_date - timedelta(days=day) for day in range(0, days_to_read_book)]

        for book_date in date_list:
            book_date_key = transform_datetime_to_iso_date_str(book_date)
            if report_start_date <= book_date <= report_stop_date:
                if book_date_key not in aggregate_result.timeline:
                    aggregate_result.timeline[book_date_key] = defaultdict(int)

                aggregate_result.timeline[book_date_key][book.classification] += average_knowlege_consumption_velocity
                # words = average_knowlege_consumption_velocity * 60 * average_reading_speed_in_minutes
                # aggregate_result.timeline[book_date_key][book.classification] += int(words)
                days_overlap += 1

        distribution_percent = days_overlap / days_to_read_book

        aggregate_result.item_count += distribution_percent
        aggregate_result.kcv += average_knowlege_consumption_velocity * days_overlap

        book_report_entry = create_book_report_entry(book, distribution_percent)
        aggregate_result.report_entries.append(book_report_entry)

    aggregate_result.report_entries.sort(key=lambda book_report_entry: book_report_entry.start_date, reverse=True)

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
            if report_start_date <= book_date <= report_stop_date:
                if book_date_key not in aggregate_result.timeline:
                    aggregate_result.timeline[book_date_key] = defaultdict(int)

                aggregate_result.timeline[book_date_key][
                    audio_book.classification] += average_knowlege_consumption_velocity

                days_overlap += 1

        distribution_percent = days_overlap / days_to_hear_book

        aggregate_result.item_count += distribution_percent
        aggregate_result.kcv += average_knowlege_consumption_velocity * days_overlap

        audio_book_report_entry = create_book_report_entry(audio_book, distribution_percent, is_book=False)
        aggregate_result.report_entries.append(audio_book_report_entry)

    aggregate_result.report_entries.sort(key=lambda audio_book_report_report: audio_book_report_report.start_date,
                                         reverse=True)

    return aggregate_result


def process_videos(videos):
    aggregate_result = AggregateResult('Videos')

    for video in videos:
        video.title = video.full_text
        video.start_date = video.created_at
        video.stop_date = video.created_at

        video.length = 2.5

        if video.full_text.find("^") != -1:
            try:
                counter = video.full_text[video.full_text.find("^") + 1:].split("\n")[0].replace("m", "")
                video.length = int(counter)
            except:
                print(f'Could not parse counter: {video.full_text}')

        total_hours = video.length / 60
        knowlege_consumption_velocity = total_hours

        video_date_key = transform_datetime_to_iso_date_str(video.created_at)

        if video_date_key not in aggregate_result.timeline:
            aggregate_result.timeline[video_date_key] = defaultdict(int)

        aggregate_result.timeline[video_date_key][video.classification] += knowlege_consumption_velocity

        aggregate_result.item_count += 1
        aggregate_result.kcv += knowlege_consumption_velocity

        video_report_entry = create_book_report_entry(video, 1, is_book=False, is_video=True)
        aggregate_result.report_entries.append(video_report_entry)

    aggregate_result.report_entries.sort(key=lambda video_report_entry: video_report_entry.start_date, reverse=True)

    return aggregate_result

def process_pairings(pairings):
    aggregate_result = AggregateResult('Pairing')

    for pairing in pairings:
        pairing.title = pairing.full_text
        pairing.start_date = pairing.created_at
        pairing.stop_date = pairing.created_at

        pairing.length = 15

        if pairing.full_text.find("^") != -1:
            try:
                counter = pairing.full_text[pairing.full_text.find("^") + 1:].split("\n")[0].replace("m", "")
                pairing.length = int(counter)
            except:
                print(f'Could not parse counter: {pairing.full_text}')

        total_hours = pairing.length / 60
        knowlege_consumption_velocity = total_hours

        pairing_date_key = transform_datetime_to_iso_date_str(pairing.created_at)

        if pairing_date_key not in aggregate_result.timeline:
            aggregate_result.timeline[pairing_date_key] = defaultdict(int)

        aggregate_result.timeline[pairing_date_key][pairing.classification] += knowlege_consumption_velocity

        aggregate_result.item_count += 1
        aggregate_result.kcv += knowlege_consumption_velocity

        pairing_report_entry = create_book_report_entry(pairing, 1, is_book=False, is_pairing=True)
        aggregate_result.report_entries.append(pairing_report_entry)

    aggregate_result.report_entries.sort(key=lambda pairing_report_entry: pairing_report_entry.start_date, reverse=True)

    return aggregate_result

def process_conferences(conferences):
    aggregate_result = AggregateResult('Conferences')

    for conference in conferences:
        conference.title = conference.full_text
        conference.start_date = conference.created_at
        conference.stop_date = conference.created_at

        conference.length = 30

        if conference.full_text.lower().startswith("i'm at"):
            conference.length = 60

        if conference.full_text.find("^") != -1:
            try:
                counter = conference.full_text[conference.full_text \
                            .find("^") + 1:] \
                            .split("\n")[0] \
                            .replace("m", "") \
                            .replace("in", "") \
                            .split(" ")[0]
                conference.length = int(counter)
            except:
                print(f'Could not parse counter: {conference.full_text}')

        total_hours = conference.length / 60
        knowlege_consumption_velocity = total_hours

        conference_date_key = transform_datetime_to_iso_date_str(conference.created_at)

        if conference_date_key not in aggregate_result.timeline:
            aggregate_result.timeline[conference_date_key] = defaultdict(int)

        aggregate_result.timeline[conference_date_key][conference.classification] += knowlege_consumption_velocity

        aggregate_result.item_count += 1
        aggregate_result.kcv += knowlege_consumption_velocity

        conference_report_entry = create_book_report_entry(conference, 1, is_book=False, is_conference=True)
        aggregate_result.report_entries.append(conference_report_entry)

    aggregate_result.report_entries.sort(key=lambda conference_report_entry: conference_report_entry.start_date, reverse=True)

    return aggregate_result

def create_book_report_entry(book, distribution_percent, *, is_book=True, is_video=False, is_pairing=False, is_conference=False):
    report_entry = ReportEntry()

    title = book.title.title()

    report_entry.title = title
    report_entry.classification = book.classification
    report_entry.start_date = book.start_date.date()
    report_entry.stop_date = book.stop_date.date()

    if is_book:
        report_entry.length = f'{book.pages} pages'
    elif is_video:
        report_entry.medium = 'Video'
        report_entry.length = f'{book.length} minutes'
    elif is_pairing:
        report_entry.medium = 'Paired'
        report_entry.length = f'{book.length} minutes'
    elif is_conference:
        report_entry.medium = 'Conferences'
        report_entry.length = f'{book.length} minutes'
    else:
        report_entry.medium = 'Audio Book'
        report_entry.length = f'{int(book.length)} minutes'
        pass

    report_entry.distribution_percent = f'{distribution_percent:.2f}'

    return report_entry
