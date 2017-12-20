from app.twitter_learning_journal.classifiers.word_classifier import WordClassifier
from app.twitter_learning_journal.dao.favorite_dao import FavoriteDao
from app.twitter_learning_journal.database.sqlalchemy_database import Database

classification_model = {
    'engineering': {'iot', 'engineer', 'stranglerapplication', 'softwaredevelopment', 'nodejs', 'flask',
                    '100daysofcode', 'dev', 'leaddev', 'bizdev', 'development', 'adventofcode', 'software',
                    'deeplearning', 'less', 'mythicalmanmonth', 'opencv', 'lambda', 'codereview', 'docker', 'bigdata',
                    'python', 'devops', 'es6', 'hacktoberfest', 'javascript', 'bots', 'devdiscuss', 'engineering',
                    'myelixirstatus', 'machinelearning', 'elasticsearch', 'vuejs', 'microservices',
                    'artificialintelligence', 'micropython', 'springone', 'codemash', 'reactjs', 'alldaydevops', 'mqtt',
                    'ruby'},
    'leadership': {'leadership', 'lead', 'anyonecanlead'},
    'agile': {'agile', 'experimentation', 'connection', 'doersdecide', 'demo', 'agile2017', 'experiment', 'continuous',
              'scrum', 'waste', 'continuousdelivery', 'flow', 'productbacklogitems', 'transformation',
              'continuousimprovement', 'everydayagile', 'agileleadership', 'designthinking', 'personas',
              'systemsthinking', 'digitaltransformation', 'wip', 'tasktop', 'orgdesign', 'growth', 'kanban',
              'goalsetting', 'process', 'cynefin', 'change', 'autonomy', 'agileaus', 'xp', 'aatc2017', 'scrumban',
              'people', 'disciplinedagile', 'kaizen', 'agilequotes', 'modernagile', 'leanagile', 'outcome', 'lean',
              'value', 'onagile', 'trust'},
    'management': {'management', 'teams', 'teamwork'},
    'happiness': {'happiness', 'happycows', 'happinessadvantage', 'lifehacks'},
    'culture': {'onshift, onshiftgsd', 'onshiftcares', 'onshiftpicnic', 'onshiftengineering', 'innovation', 'onshift',
                'inverseconwaymaneuver', 'onshiftgsd', 'livelong', 'zenmonday', 'gsd', 'cultureaced', 'oshackday'},
    'quality': {'softwaretesting', 'testautomation', 'watir', 'testing', 'cucumber', 'qa', 'makeyourownlane',
                'pageobject', 'selenium'},
    'other': {'valid', 'responsibility', 'ideservethis', 'computervision', 'jengacode', 'photo', 'dumb', 'westyaward',
              'gameofthrones', 'gobblegobble', 'classic', 'virtual', 'turkishswiftie', 'got', 'friends',
              'musiccitycode', 'itsjustnotthathard', 'vogue', 'anger', 'july4th', 'disappointed', 'happythanksgiving',
              'laborday', 'successtips', 'cle', 'singer', 'modernsecurityseries', 'summer', 'sketchnote', 'failure',
              'foreverswiftie', 'mha17', 'recommended', 'savethehorsies', 'lego', 'internet'},
    'conferences': {'bettersoftwarecon', 'goat17', 'oredev', 'onagile2017', 'lightningtalks', 'oredev2017', 'srecon',
                    'gotochgo', 'conference', 'pyconie', 'does17', 'pyohio', 'yow17', 'dataengconf', 'yow16'},
    'startup': {'growthhacking', 'startup', 'entrepreneur', 'ceo', 'vc'},
    'coach': {'mentorship', 'excellence', 'coaching', 'mentoring', 'techcoach', 'hourofcode', 'craft', 'refactoring',
              'pairprogramming', 'agilecoach', 'transparency', 'mobprogramming', 'legacycode', 'extremeprogramming',
              'tdd', 'comments', 'safe', 'scrummaster', 'programmerhumor', 'boyscoutrule', 'makingworkvisible',
              'strongstylepairing'},
    'learning': {'hypothesis', 'learning', 'reading', 'fail'},
    'product': {'productmanagement', 'prodmgmt', 'product', 'servicedesign', 'ux', 'cx', 'ui', 'orddesign',
                'productnerd', 'arch', 'productcraft', 'customerfirst', 'design'},
    'diversity': {'diversity'},
}

if __name__ == '__main__':
    database = Database()
    favorite_dao = FavoriteDao(database)

    _favorites = favorite_dao.query_all()
    total = len(_favorites)
    print(f'Total Favorites: {total}')

    for count, favorite in enumerate(_favorites):
        if not favorite.hashtags:
            continue

        print(f'{count} of {total}')

        for hashtag in favorite.hashtags.split('|'):
            _hashtag = hashtag.lower().strip()
            word_classifier = WordClassifier(_hashtag, classification_model)
            classification = word_classifier.classify()

            if not sum([classification[key] for key in classification.keys()]):
                print(f'Not classified: {_hashtag}')
                print(f'            - : {favorite.full_text}\n')

                tag = input('Enter classification tag: ')
                tag = tag.lower().strip()

                if tag not in classification_model:
                    print(f'Adding classification tag: {tag}')
                    classification_model[tag] = set()

                classification_model[tag].add(_hashtag)

                print(classification_model[tag])
