[![Build Status](https://travis-ci.org/DEV3L/twitter-learning-journal.svg?branch=master)](https://travis-ci.org/DEV3L/twitter-learning-journal)
[![Coverage Status](https://coveralls.io/repos/github/DEV3L/twitter-learning-journal/badge.svg)](https://coveralls.io/github/DEV3L/twitter-learning-journal)
[![Code Climate](https://codeclimate.com/github/DEV3L/twitter-learning-journal/badges/gpa.svg)](https://codeclimate.com/github/DEV3L/twitter-learning-journal)

# twitter-learning-journal
Qualify learnings of a Twitter account as a learning journal.

By doing this, there are a great deal of things we can measure!
* Articles words read
* Video minutes watched
* Audio minutes listened
* Book pages read
* Blogs published words
* Tweeted words

# Plan

1. Scrape a twitter feed using Tweepy
    * Eventually need to get beyond 3k tweets
2. Classify tweets
    * Brute force at first, eventually algorithmic
3. Visualize the learning over time


# Environment Variables
* Twitter Api Credentials
  * TWITTER_ACCESS_TOKEN
  * TWITTER_CONSUMER_KEY
  * TWITTER_CONSUMER_SECRET
  * TWITTER_TOKEN_SECRET


# References

* [Introduction to SQLite In Python](https://www.pythoncentral.io/introduction-to-sqlite-in-python/)
* [SQLAlchemy Tutorial](http://docs.sqlalchemy.org/en/latest/orm/tutorial.html)
* [Python 3 Using 'yield from' In Generators](http://simeonvisser.com/posts/python-3-using-yield-from-in-generators-part-1.html)




## Contributing

1. Fork it!
2. Create your feature branch: `git checkout -b my-twitter-learning-journal`
3. Commit your changes: `git commit -am 'Add something'`
4. Push to the branch: `git push origin my-twitter-learning-journal`
5. Submit a pull request :D
