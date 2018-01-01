import collections
from datetime import datetime

AudioDetail = collections.namedtuple('AudioDetail', 'start_date stop_date title classification total_audio_minutes')


def get_audio_books():
    audio_books = []

    # ###
    # audio books
    # ###

    # making work visible
    audio_books.append(create_audio_detail(_datetime(2017, 12, 11), _datetime(2017, 12, 16),
                                           'making work visible', 'agile', 310))

    # start with why
    audio_books.append(create_audio_detail(_datetime(2017, 11, 27), _datetime(2017, 12, 3),
                                           'start with why', 'leadership', 438))

    # a seat at the table
    audio_books.append(create_audio_detail(_datetime(2017, 10, 17), _datetime(2017, 11, 21),
                                           'a seat at the table', 'leadership', 560))

    # lean in
    audio_books.append(create_audio_detail(_datetime(2017, 9, 20), _datetime(2017, 10, 16),
                                           'lean in', 'leadership', 387))

    # five dysfunctions of a team
    audio_books.append(create_audio_detail(_datetime(2017, 9, 14), _datetime(2017, 9, 20),
                                           'five dysfunctions of a team', 'leadership', 225))

    # the happiness advantage
    audio_books.append(create_audio_detail(_datetime(2017, 8, 19), _datetime(2017, 9, 14),
                                           'the happiness advantage', 'leadership', 443))

    # scrum
    audio_books.append(create_audio_detail(_datetime(2017, 8, 2), _datetime(2017, 8, 18),
                                           'scrum', 'agile', 403))

    # work rules!
    audio_books.append(create_audio_detail(_datetime(2017, 7, 18), _datetime(2017, 8, 2),
                                           'work rules!', 'leadership', 686))

    # drive
    audio_books.append(create_audio_detail(_datetime(2017, 6, 28), _datetime(2017, 7, 17),
                                           'drive', 'leadership', 353))

    # crucial conversations
    audio_books.append(create_audio_detail(_datetime(2017, 6, 12), _datetime(2017, 6, 25),
                                           'crucial conversations', 'leadership', 353))

    # 'began listening to crucial conversations': ('2017-06-12', 'audio book', 'start'),
    # 'finished listening to crucial conversations': ('2017-06-25', 'audio book', 'stop'),
    #
    # # switch
    # # Started listening to on Audible:\nSwitch: How to Change Things When Change Is Hard
    # 'started listening to on audible:': ('2017-05-24', 'audio book', 'start'),
    # 'finished listening to switch': ('2017-06-08', 'audio book', 'stop'),
    #
    # # the subtle art of not giving a f*ck
    # # Finished listening to on Audible:\nThe Subtle Art of Not Giving a F*ck
    # 'started listening to the subtle art of not giving a f*ck': ('2017-04-23', 'audio book', 'start'),  # inferred
    # 'finished listening to on audible:': ('2017-05-23', 'audio book', 'stop'),
    #
    #
    # # a seat at the table
    # ('2017-11-21', 'audio book', 'stop'),

    switch_book = AudioDetail(
        start_date=datetime(year=2017, month=5, day=24),
        stop_date=datetime(year=2017, month=6, day=8),
        title='switch: how to change things when change is hard',
        classification='agile',
        total_audio_minutes=456
    )
    audio_books.append(switch_book)

    return audio_books


def _datetime(year, month, day):
    return datetime(year=year, month=month, day=day)


def create_audio_detail(start_date, stop_date, title, classification, total_audio_minutes):
    audio_detail = AudioDetail(
        start_date=start_date,
        stop_date=stop_date,
        title=title,
        classification=classification,
        total_audio_minutes=total_audio_minutes
    )
    return audio_detail
