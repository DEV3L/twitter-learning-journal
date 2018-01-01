from collections import defaultdict
from datetime import datetime

from scripts import clean_title


class BookDetail:
    start_date = None
    stop_date = None
    title = None
    classification = None
    pages = None


def get_books():
    _books = defaultdict(BookDetail)

    for title, event_date, media_type, event_type, pages, classification in book_data:
        _title = clean_title(title)

        book = _books.get(_title)

        if book is None:
            book = BookDetail()

        book.title = _title
        book.classification = classification
        book.pages = pages

        _event_date = datetime.strptime(event_date, '%Y-%m-%d')

        if 'start' == event_type:
            book.start_date = _event_date
        else:
            book.stop_date = _event_date

        _books[_title] = book

    return _books.values()



book_data = {
    # cracking the pm interview
    ('started reading: cracking the pm interview', '2017-12-16', 'book', 'start', 364, 'agile'),
    ('finished reading: cracking the pm interview', '2017-12-30', 'book', 'stop', 364, 'agile'),

    # how f*cked up is your management
    ('started reading: how f*cked up is your management by @johnath  and @shappy tonight! #techcoach @hfuiym',
     '2017-11-11', 'book', 'start', 250, 'leadership'),
    (
        'finished reading: how f*cked up is your management - an uncomfortable conversation about modern leadership by @hfuiym',
        '2017-12-15', 'book', 'stop', 250, 'leadership'),

    # clean coder
    ('started reading the clean coder by @unclebobmartin', '2017-11-15', 'book', 'start', 210, 'engineering'),
    ('finished reading the clean coder', '2018-02-15', 'book', 'stop', 210, 'engineering'),

    # production ready microservices
    ('began reading production ready microservices by @susanthesquark', '2017-10-12', 'book', 'start', 153,
     'engineering'),
    ('finished reading production ready microservices by @susanthesquark', '2017-11-02', 'book', 'stop', 153,
     'engineering'),

    # head first python
    ('began reading head first python', '2017-07-26', 'book', 'start', 494, 'engineering'),
    ('finished reading head first python', '2017-10-03', 'book', 'stop', 494, 'engineering'),

    # the startup way
    ('started reading the startup way', '2017-08-09', 'book', 'start', 400, 'leadership'),
    ('finished reading the startup way', '2018-01-03', 'book', 'stop', 400, 'leadership'),

    # prgamatic thinking and learning
    ('pragmatic thinking and learning', '2017-08-17', 'book', 'start', 251, 'agile'),  # inferred
    ('pragmatic thinking and learning', '2017-10-08', 'book', 'stop', 251, 'agile'),  # inferred

    # mythical man-month
    ('started reading the mythical man-month', '2017-07-03', 'book', 'start', 332, 'engineering'),
    ('finished reading the mythical man-month', '2017-08-13', 'book', 'stop', 332, 'engineering'),

    # clean code
    ('started reading clean code', '2017-06-07', 'book', 'start', 434, 'engineering'),
    ('finished reading clean code', '2017-08-05', 'book', 'stop', 434, 'engineering'),

    # user story mapping
    ('started reading user story mapping', '2017-05-14', 'book', 'start', 324, 'agile'),
    ('finished reading user story mapping', '2017-05-03', 'book', 'stop', 324, 'agile'),

    # object thinking
    ('started reading object thinking', '2017-05-02', 'book', 'start', 334, 'engineering'),
    ('finished reading object thinking', '2017-05-14', 'book', 'stop', 334, 'engineering'),

    # the pragmatic programmer
    ('started reading the pragmatic programmer', '2017-04-02', 'book', 'start', 321, 'engineering'),  # inferred
    ('finished reading the pragmatic programmer', '2017-05-02', 'book', 'stop', 321, 'engineering'),
}
