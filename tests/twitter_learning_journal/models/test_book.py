from datetime import datetime

from pytest import mark

from app.twitter_learning_journal.models.book import Book


def test_book():
    id = 1
    screen_name = 'screen_name'
    title = 'title'
    classification = 'classification'
    pages = 5
    start_date = datetime.now()
    stop_date = datetime.now()

    expected_str = f'<Book(id={id}, ' \
                   f'screen_name={screen_name}, ' \
                   f'title={title}, ' \
                   f'classification={classification}, ' \
                   f'pages={pages}, ' \
                   f'start_date={start_date}, ' \
                   f'stop_date={stop_date})>'

    book = Book(
        id=1,
        screen_name=screen_name,
        title=title,
        classification=classification,
        pages=pages,
        start_date=start_date,
        stop_date=stop_date
    )

    assert expected_str == str(book)


@mark.parametrize("book_id, other_book_id, expected_result",
                  [
                      (None, None, False),
                      (1, None, False),
                      (None, 1, False),
                      (1, 1, True),
                      (1, 2, False),
                  ])
def test_book_equal(book_id, other_book_id, expected_result):
    assert expected_result == (Book(id=book_id) == Book(id=other_book_id))
