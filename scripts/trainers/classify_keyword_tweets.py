from app.twitter_learning_journal.dao.tweet_dao import TweetDao
from app.twitter_learning_journal.database.sqlalchemy_database import Database
from app.twitter_learning_journal.models.detail import Detail


def classify_keyword_tweets():
    database = Database(echo=False)
    tweet_dao = TweetDao(database)
    details = tweet_dao._database.query(Detail).all()
    details = [detail for detail in details if detail.type == 'keyword']

    count = 0

    for detail in details:
        count += 1
        _title = detail.title.strip()

        print(f'{detail.start_date}:{_title}')

        if _title in manual_keyword_detail_classification.keys():
            continue

        is_continue = False
        for key in manual_keyword_detail_classification.keys():
            if key in _title:
                is_continue = True
                # magic is still to be implemented here
                break

        if is_continue:
            continue


manual_keyword_detail_classification = {
    'smart guys like ': None,
    'this is a': None,
    'great insight on writing clean code from one of the greats': None,
    'i read this somewhere, seen it today': None,
    '&gt;&gt;&gt; import this': None,
    'product reading group': None,
    'view the code as a reader, not as an author': None,
    '#readinggroup @onshift': None,
    'building and building without listening': None,
    'i sympathy read it with a junior dev': None,
    'product reading from': None,
    'product reading group tom': None,
    'looking forward to reading it': None,
    'maybe on his/her commute in to work': None,
    'are trying to connect to the onagile conference': None,
    'truly great developers are difficult to find': None,
    'is to immediately roll back': None,
    'i run lean coffee': None,
    'i am halfway through': None,
    'literature i read': None,
    'i wish founders would read': None,
    'current status:': None,
    'how many #agile practitioners and coaches have actually read the agile manifesto?': None,
    'thinking about accounting for audio books next': None,
    '@johncutlefish interesting project!': None,
    'oh this makes me happy': None,
    '#leancoffee topics': None,
    'thank you for sharing': None,
    'what other lean books have you read': None,
    'looking forward to an exciting read over': None,
    'a must watch for all devops leaders': None,
    'some people really benefit from hearing advice that everyone knows': None,
    'i believe i saw in the thread': None,
    'if you have to do something manually more than once, automate it so you never have to do it again': None,
    '#aatc2017 #onshift': None,
    'finished listening to the phoenix project on #audible, thanks @realgenekim! #pheonixproject': None,  # mistweet

    # videos
    'i would highly recommend watching': ('2017-11-12', 'video', ''),

    # ###
    # audio books
    # ###

    # making work visible
    'started listening to: making work visible': ('2017-12-11', 'audio book', 'start'),
    'finished listening to: making work visible': ('2017-12-16', 'audio book', 'stop'),

    # start with why
    'started listening to start with why': ('2017-11-27', 'audio book', 'start'),
    "finished listening to 'start with why: how great leaders inspire everyone to take action'":
        ('2017-12-03', 'audio book', 'stop'),

    # a seat at the table
    'started listening to a seat at the table': ('2017-10-17', 'audio book', 'start'),  # inferred
    'finished listening to a seat at the table': ('2017-11-21', 'audio book', 'stop'),

    # lean in
    'started listening to lean in': ('2017-09-20', 'audio book', 'start'),
    'finished listening to lean in': ('2017-10-16', 'audio book', 'stop'),

    # the five dysfunctions of a team
    'started listening to the five dysfunctions of a team': ('2017-09-14', 'audio book', 'start'),
    'finished listening to the five dysfunctions of a team': ('2017-09-20', 'audio book', 'stop'),

    # the happiness advantage
    'started listening to the happiness advantage': ('2017-08-19', 'audio book', 'start'),  # inferred
    'finished listening to the happiness advantage': ('2017-09-14', 'audio book', 'stop'),

    # scrum
    'started listening to scrum': ('2017-08-02', 'audio book', 'start'),
    'finished listening to scrum': ('2017-08-18', 'audio book', 'stop'),

    # work rules!
    'started listening to work rules!': ('2017-07-18', 'audio book', 'start'),
    'finished listening to work rules!': ('2017-08-02', 'audio book', 'stop'),

    # drive
    'started listening to drive': ('2017-06-28', 'audio book', 'start'),
    'finished listening to drive': ('2017-07-17', 'audio book', 'stop'),

    # crucial conversations
    'began listening to crucial conversations': ('2017-06-12', 'audio book', 'start'),
    'finished listening to crucial conversations': ('2017-06-25', 'audio book', 'stop'),

    # switch
    # Started listening to on Audible:\nSwitch: How to Change Things When Change Is Hard
    'started listening to on audible:': ('2017-05-24', 'audio book', 'start'),
    'finished listening to switch': ('2017-06-08', 'audio book', 'stop'),

    # the subtle art of not giving a f*ck
    # Finished listening to on Audible:\nThe Subtle Art of Not Giving a F*ck
    'started listening to the subtle art of not giving a f*ck': ('2017-04-23', 'audio book', 'start'),  # inferred
    'finished listening to on audible:': ('2017-05-23', 'audio book', 'stop'),

    # ###
    # books
    # ###
    # 250-300 words per page, 250 words per page, 150-450 words per page -- 3 rando sources
    # 200

    # cracking the pm interview
    'started reading: cracking the pm interview': ('2017-12-16', 'book', 'start'),
    'finished reading: cracking the pm interview': ('2017-12-30', 'book', 'stop'),

    # how f*cked up is your management
    'started reading: how f*cked up is your management by @johnath  and @shappy tonight! #techcoach @hfuiym': (
        '2017-11-11', 'book', 'start'),
    'finished reading: how f*cked up is your management - an uncomfortable conversation about modern leadership by @hfuiym': (
        '2017-12-15', 'book', 'stop'),

    # clean coder
    'started reading the clean code by @unclebobmartin': ('2017-11-15', 'book', 'start'),  # should be clean coder!
    'finished reading the clean coder': ('2018-02-15', 'book', 'stop'),

    # production ready microservices
    'began reading production ready microservices by @susanthesquark': ('2017-10-12', 'book', 'start'),
    'finished reading production ready microservices by @susanthesquark': ('2017-11-02', 'book', 'stop'),

    # head first python
    'began reading head first python': ('2017-07-26', 'book', 'start'),
    'finished reading head first python': ('2017-10-03', 'book', 'stop'),

    # the startup way
    'started reading the startup way': ('2017-08-09', 'book', 'start'),
    'finished reading the startup way': ('2017-01-03', 'book', 'stop'),

    # mythical man-month
    'started reading the mythical man-month': ('2017-07-03', 'book', 'start'),
    'finished reading the mythical man-month': ('2017-08-13', 'book', 'stop'),

    # clean code
    'started reading clean code': ('2017-06-07', 'book', 'start'),
    'finished reading clean code': ('2017-08-05', 'book', 'stop'),

    # user story mapping
    'started reading user story mapping': ('2017-05-14', 'book', 'start'),
    'finished reading user story mapping': ('2017-05-03', 'book', 'stop'),

    # object thinking
    'started reading object thinking': ('2017-05-02', 'book', 'start'),
    'finished reading object thinking': ('2017-05-14', 'book', 'stop'),

    # the pragmatic programmer
    'started reading the pragmatic programmer': ('2017-03-02', 'book', 'stop'),  # inferred
    'finished reading the pragmatic programmer': ('2017-05-02', 'book', 'stop'),
}
