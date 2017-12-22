ignore_characters = [
    '.',
    ',',
    '!',
    '*',
    '(',
    ')',
    '=',
    '+',
    '`',
    '~',
    '"',
    "'"
]

global_classification_model = {
    'engineering': {'iot', 'engineer', 'stranglerapplication', 'softwaredevelopment', 'nodejs', 'flask',
                    '100daysofcode', 'dev', 'leaddev', 'bizdev', 'development', 'adventofcode', 'software',
                    'deeplearning', 'less', 'mythicalmanmonth', 'opencv', 'lambda', 'codereview', 'docker', 'bigdata',
                    'python', 'devops', 'es6', 'hacktoberfest', 'javascript', 'bots', 'devdiscuss', 'engineering',
                    'myelixirstatus', 'machinelearning', 'elasticsearch', 'vuejs', 'microservices',
                    'modernsecurityseries',
                    'artificialintelligence', 'micropython', 'springone', 'codemash', 'reactjs', 'alldaydevops', 'mqtt',
                    'ruby', 'bettersoftwarecon', 'goat17', 'oredev', 'onagile2017', 'lightningtalks', 'oredev2017',
                    'srecon', 'gotochgo', 'conference', 'pyconie', 'does17', 'pyohio', 'yow17', 'dataengconf', 'yow16'
                    },
    'leadership': {'leadership', 'lead', 'anyonecanlead',
                   'growthhacking', 'startup', 'entrepreneur', 'ceo', 'vc',
                   'management', 'teams', 'teamwork', 'responsibility',
                   'onshift, onshiftgsd', 'onshiftcares', 'onshiftpicnic', 'onshiftengineering', 'innovation',
                   'onshift',
                   'inverseconwaymaneuver', 'onshiftgsd', 'livelong', 'zenmonday', 'gsd', 'cultureaced', 'oshackday',
                   'happiness', 'happycows', 'happinessadvantage', 'lifehacks'
                   },
    'agile': {'agile', 'experimentation', 'connection', 'doersdecide', 'demo', 'agile2017', 'experiment', 'continuous',
              'scrum', 'waste', 'continuousdelivery', 'flow', 'productbacklogitems', 'transformation',
              'continuousimprovement', 'everydayagile', 'agileleadership', 'designthinking', 'personas',
              'systemsthinking', 'digitaltransformation', 'wip', 'tasktop', 'orgdesign', 'growth', 'kanban',
              'goalsetting', 'process', 'cynefin', 'change', 'autonomy', 'agileaus', 'xp', 'aatc2017', 'scrumban',
              'people', 'disciplinedagile', 'kaizen', 'agilequotes', 'modernagile', 'leanagile', 'outcome', 'lean',
              'value', 'onagile', 'trust', 'mentorship', 'excellence', 'coaching', 'mentoring', 'techcoach',
              'hourofcode', 'craft', 'refactoring',
              'pairprogramming', 'agilecoach', 'transparency', 'mobprogramming', 'legacycode', 'extremeprogramming',
              'tdd', 'comments', 'safe', 'scrummaster', 'programmerhumor', 'boyscoutrule', 'makingworkvisible',
              'strongstylepairing', 'hypothesis', 'learning', 'reading', 'fail',
              'softwaretesting', 'testautomation', 'watir', 'testing', 'cucumber', 'qa', 'makeyourownlane',
              'pageobject', 'selenium'},
    'product': {'productmanagement', 'prodmgmt', 'product', 'servicedesign', 'ux', 'cx', 'ui', 'orddesign',
                'productnerd', 'arch', 'productcraft', 'customerfirst', 'design'},
    'diversity': {'diversity'},
    'other': {'valid', 'ideservethis', 'computervision', 'jengacode', 'photo', 'dumb', 'westyaward',
              'gameofthrones', 'gobblegobble', 'classic', 'virtual', 'turkishswiftie', 'got', 'friends',
              'musiccitycode', 'itsjustnotthathard', 'vogue', 'anger', 'july4th', 'disappointed', 'happythanksgiving',
              'laborday', 'successtips', 'cle', 'singer', 'summer', 'sketchnote', 'failure',
              'foreverswiftie', 'mha17', 'recommended', 'savethehorsies', 'lego', 'internet'},
}


def get_classification_model(classification_model):
    return classification_model or global_classification_model
