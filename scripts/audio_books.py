from datetime import datetime

from scripts import clean_title


class AudioBookDetail:
    start_date = None
    stop_date = None
    title = None
    classification = None
    length = None


def get_audio_books():
    audio_books = {}

    for title, event_date, media_type, event_type, minutes, classification in audio_book_data:
        title = clean_title(title)

        audio_book = audio_books.get(title)

        if audio_book is None:
            audio_book = AudioBookDetail()

        audio_book.title = title
        audio_book.classification = classification
        audio_book.length = minutes

        _event_date = datetime.strptime(event_date, '%Y-%m-%d')

        if 'start' == event_type:
            audio_book.start_date = _event_date
        else:
            audio_book.stop_date = _event_date

        audio_books[title] = audio_book

    return [book for book in audio_books.values()]


audio_book_data = {
    # making work visible

    ('started listening to: making work visible', '2017-12-11', 'audio book', 'start', 310, 'agile'),
    ('finished listening to: making work visible', '2017-12-16', 'audio book', 'stop', 310, 'agile'),

    # start with why
    ('started listening to start with why', '2017-11-27', 'audio book', 'start', 438, 'leadership'),
    ("finished listening to 'start with why'", '2017-12-03', 'audio book', 'stop', 438, 'leadership'),

    # a seat at the table
    ('started listening to a seat at the table', '2017-10-17', 'audio book', 'start', 560, 'leadership'),  # inferred
    ('finished listening to a seat at the table', '2017-11-21', 'audio book', 'stop', 560, 'leadership'),

    # lean in
    ('started listening to lean in', '2017-09-20', 'audio book', 'start', 387, 'leadership'),
    ('finished listening to lean in', '2017-10-16', 'audio book', 'stop', 387, 'leadership'),

    # the five dysfunctions of a team
    ('started listening to the five dysfunctions of a team', '2017-09-14', 'audio book', 'start', 225, 'leadership'),
    ('finished listening to the five dysfunctions of a team', '2017-09-20', 'audio book', 'stop', 225, 'leadership'),

    # the happiness advantage
    ('started listening to the happiness advantage', '2017-08-19', 'audio book', 'start', 443, 'leadership'),
# inferred
    ('finished listening to the happiness advantage', '2017-09-14', 'audio book', 'stop', 443, 'leadership'),

    # scrum
    ('started listening to scrum', '2017-08-02', 'audio book', 'start', 403, 'agile'),
    ('finished listening to scrum', '2017-08-18', 'audio book', 'stop', 403, 'agile'),

    # work rules!
    ('started listening to work rules!', '2017-07-18', 'audio book', 'start', 686, 'leadership'),
    ('finished listening to work rules!', '2017-08-02', 'audio book', 'stop', 686, 'leadership'),

    # drive
    ('started listening to drive', '2017-06-28', 'audio book', 'start', 335, 'leadership'),
    ('finished listening to drive', '2017-07-17', 'audio book', 'stop', 335, 'leadership'),

    # crucial conversations
    ('began listening to crucial conversations', '2017-06-12', 'audio book', 'start', 353, 'leadership'),
    ('finished listening to crucial conversations', '2017-06-25', 'audio book', 'stop', 353, 'leadership'),

    # switch
    # Started listening to on Audible:\nSwitch: How to Change Things When Change Is Hard
    ('started listening to switch:', '2017-05-24', 'audio book', 'start', 462, 'leadership'),
    ('finished listening to switch', '2017-06-08', 'audio book', 'stop', 462, 'leadership'),

    # the subtle art of not giving a f*ck
    # Finished listening to on Audible:\nThe Subtle Art of Not Giving a F*ck
    (
    'started listening to the subtle art of not giving a f*ck', '2017-04-23', 'audio book', 'start', 330, 'leadership'),
# inferred
    (
    'finished listening to the subtle art of not giving a f*ck', '2017-05-23', 'audio book', 'stop', 330, 'leadership'),
}
