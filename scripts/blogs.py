from urllib import request
from urllib.request import Request

from bs4 import BeautifulSoup

from app.twitter_learning_journal.dao.tweet_dao import TweetDao
from app.twitter_learning_journal.database.sqlalchemy_database import Database
from app.twitter_learning_journal.models.detail import Detail
from app.twitter_learning_journal.transformers.transform_str import remove_ignore_characters_from_str


def count_html_words():
    database = Database()
    tweet_dao = TweetDao(database)
    details = tweet_dao._database.query(Detail).all()

    print(f'total details: {len(details)}')
    detail_count = 1

    for detail in details:
        if not detail.url:
            pass

        total_words = 0

        for url in detail.url.split('|'):
            is_blog = True

            for video_url in not_blog_urls:
                if video_url in url:
                    print(f'@@@@ URL looks like not blog: {url}')
                    detail.is_fully_classified = False
                    detail.type = 'other'
                    database.add(detail)
                    is_blog = False

            if not is_blog:
                continue

            url = url.replace('www.google.com/amp/s/', '')

            _request = Request(url)
            _request.headers = headers

            try:
                html = request.urlopen(_request).read().decode('utf8')
            except Exception as e:
                print(f'could not open url: {url}')
                continue

            html = remove_auxiiary_tags(html)

            _raw = BeautifulSoup(html).get_text()
            _raw = remove_ignore_characters_from_str(_raw)
            _raw = ' '.join(_raw.split())

            raw_split = _raw.split()
            words = len(raw_split)

            devation = default_domain_devation
            is_found = False

            if words == 0:
                print('Removed/Redirected URL')
                continue

            # I feel like this is a common problem that could be optimized
            for key in domain_deviations.keys():
                if key in url:
                    is_found = True
                    devation = domain_deviations[key]

            if not is_found:
                print()

            if words > (devation * 1.25):
                words = words - devation

            print(f'counted words: {words}')
            total_words += words

        detail_count += 1

        print(f'processed: {detail_count}')

        if total_words == 0:
            continue

        detail.word_count = total_words
        database.add(detail)
    database.commit()


def remove_auxiiary_tags(html):
    soup = BeautifulSoup(html)
    for tag in soup(['script', 'style', 'head']):
        tag.decompose()
    return ' '.join(soup.stripped_strings)


headers = {
    'User-Agent': 'Mozilla/5.0 (Linux; Android 6.0.1; SM-G920V Build/MMB29K) '
                  'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.98 Mobile Safari/537.36'
}

default_domain_devation = 300

domain_deviations = {
    'cucumber.io': 200,
    'blog.jessitron.com': 250,
    '12factor.net': 25,
    'interviewcake.com': 550,
    'yanado.com': 300,
    'medium.freecodecamp.org': 200,
    'deque.blog': 300,
    'shmula.com': 500,
    'fearlesssalarynegotiation.com': 500,
    'gizmodo.com': 150,
    'expertenough.com': 150,
    'github.io': 100,
    'employeebenefitadviser.com': 250,
    'pragprog.com': 150,
    'treyhunner.com': 500,
    'scientistlive.com': 700,
    'fastcodesign.com': 350,
    'caroli.org': 250,
    'Caroli.org': 250,
    'coreyhaines.com': 700,
    'tjelvarolsson.com': 150,
    'aits.org': 400,
    'techbeacon.com': 1700,
    'curl.trillworks.com': 25,
    'oswalpalash.com': 25,
    'theoatmeal.com': 25,
    'opensource.googleblog.com': 300,
    'lean.org': 1050,
    'nyti.ms': 450,

    'quora.com': 150,
    'hackernoon.com': 175,
    'insidebigdata.com': 415,
    'fcc.im': 250,
    'lornemitchell.com': 400,
    'medium.com': 350,
    'wikipedia.org': 1250,
    'ASP.NET': default_domain_devation,
    'visualstudio.com': 1500,
    'devbridge.com': 200,
    'buff.ly': 600,
    'ben-evans.com': 200,
    'runlean.ly': 200,
    'dev.to': 200,
    'agileuprising.com': 200,
    'techcrunch.com': 100,
    'tobeagile.com': 225,
    'scrumalliance.org': 1650,
    'increment.com': 650,
    'solutionsiq.com': 550,
    'wordpress.com': 200,
    'eleganthack.com': 650,
    'brodzinski.com': 425,
    'blog.cleancoder.com': 650,
    'blog.juandelgado.es': 150,
    'blackswanfarming.com': 400,
    'thght.works': 400,
    'zumsteg.net': 350,
    'ribbonfarm.com': 1600,
    'curiosity.com': 250,
    'blogspot.com': 250,
    'builttoadapt.io': 150,
    'm.signalvnoise.com': 250,
    'mcfunley.com': 200,
    'dbader.org': 800,
    'martinfowler.com': 300,
    'thoughtworks.com': 300,
    'extremeuncertainty.com': 250,
    'facebook.com': 100,
    'michaelnygard.com': 150,
    'vitsoe.com': 150,
    'a16z.com': 150,
    'engineering.semantics3.com': 200,
    'blog.coffeeandcode.com': 150,
    'motherboard.vice.com': 150,
    'andrewchen.co': 150,
    'inc.com': 200,
    'startupsventurecapital.com': 200,
    'michaelfeathers.silvrback.com': 50,
    'blog.wingman-sw.com': 2000,
    'nataliewarnert.com': 350,
    'solutionsiq.in': 225,
    'itrevolution.com': 400,
    'linkedin.com': 50,
    'lnkd.in': 50,
    'mountaingoatsoftware.com': 500,
    'producthabits.com': 150,
    'keybase.io': 250,
    'agilealliance.org': 350,
    'codemash.org': 250,
    'stackoverflow.com': 200,
    'medium': 200,
    'fastcompany.com': 450,
    'blog.thedigitalcatonline.com': 750,
    'sandimetz.com': 150,
    'stickyminds.com': 400,
    'laughingmeme.org': 500,
    'ronjeffries.com': 250,
    'luis-goncalves.com': 850,
    'lucidchart.com': 200,
    'simpleisbetterthancomplex.com': 300,
    'jasonrudolph.com': 150,
    'engineering.onshift.com': 125,
    'eng.lyft.com': 100,
    'spikesandstories.com': 500,
    'labs.spotify.com': 1800,
    'lifehacker.com': 300,
    'wired.com': 550,
    'meowni.ca': 300,
    'microsoft.com': 500,
    'svpg.com': 200,
    'worldpositive.com': 1200,
    'aws.amazon.com': 4700,

    'leanqa.wordpress.com': 0,

    'snap-ci.com': default_domain_devation,
    'sumo.ly': default_domain_devation,
    'bit.ly': default_domain_devation,
    'shar.es': default_domain_devation,
    'go.shr.lc': default_domain_devation,
    'dlvr.it': default_domain_devation,
    'getpocket.com': default_domain_devation,
    'leanuxmas.com': default_domain_devation,
    'fb.me': default_domain_devation,
    'tinyurl.com': default_domain_devation,
    'ow.ly': default_domain_devation,

}

not_blog_urls = {
    'youtu.be',
    'youtube.com',
    'vimeo.com',

    'slideshare.net',

    # podcast
    'pca.st',

    'gist.github.com',

    'meetup.com',

    # conference
    'sched.co',

    # words out...
    'dev.to/dev3l',
    'softwaredev3loper.wordpress.com',
}
