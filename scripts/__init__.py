# assumption variables
average_words_per_page = 250
devaiation_book_pages = 50

# accounting for material density
average_reading_speed_in_minutes = 200
average_blog_reading_speed = 175
average_tweet_reading_speed = 125

github_commit_minute_count = 15

start_phrases = ['started reading', 'began reading', 'started listening to', 'began listening to']
stop_phrases = ['finished reading', 'finished listening to', ]
title_termination_tokens = [' - ', ' by ']
ignore_characters = [':', "'"]


def clean_title(title):
    title = _remove_omissions(title, ignore_characters)
    title = _remove_omissions(title, start_phrases)
    title = _remove_omissions(title, stop_phrases)
    title = _sublist_termination_tokens(title, title_termination_tokens)
    title = title.strip()
    return title


def _sublist_termination_tokens(input_string, termination_tokens):
    for termination_token in termination_tokens:

        if termination_token in input_string:
            stop_index = input_string.find(termination_token)
            input_string = input_string[:stop_index]

    return input_string


def _remove_omissions(input_string, omissions):
    for omission in omissions:
        input_string = input_string.replace(omission, '')

    return input_string
