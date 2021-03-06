ignore_characters = [
    '.',
    ',',
    '!',
    '*',
    '(',
    ')',
    # '-',
    '=',
    '+',
    '?',
    '‘',
    '|',
    '’',
    '`',
    '~',
    '"',
    '“',
    '”',
    ':',
    '/',
    '#',
    '@',
    "'"
]

global_classification_model = {
    'engineering': {'iot', 'engineer', 'stranglerapplication', 'softwaredevelopment', 'nodejs', 'flask',
                    '100daysofcode', 'dev', 'leaddev', 'bizdev', 'development', 'adventofcode', 'software',
                    'deeplearning', 'less', 'mythicalmanmonth', 'opencv', 'lambda', 'codereview', 'docker', 'bigdata',
                    'python', 'devops', 'es6', 'hacktoberfest', 'javascript', 'bots', 'devdiscuss', 'engineering',
                    'myelixirstatus', 'machinelearning', 'elasticsearch', 'vuejs', 'microservices',
                    'modernsecurityseries', 'tests', 'edges', 'edge', 'logging', 'services', 'distributed', 'systems'
                    'artificialintelligence', 'micropython', 'springone', 'codemash', 'reactjs', 'alldaydevops', 'mqtt',
                    'ruby', 'bettersoftwarecon', 'goat17', 'oredev', 'onagile2017', 'lightningtalks', 'oredev2017',
                    'srecon', 'gotochgo', 'conference', 'pyconie', 'does17', 'pyohio', 'yow17', 'dataengconf', 'yow16',
                    'computer', 'docker', 'functions', 'source',
                    'science', 'cache', 'invalidation', 'off-by-1', 'errors', 'json', 'web', 'service', 'code', 'repo',
                    'repository', 'continuousdeployment', 'continuousdelivery', 'c', 'junior', 'github', 'pypi', 'crud',
                    'bot', 'technical', 'google', 'patch', 'sha', 'id10t', 'oscon', 'dijkstra',
                    'artificial', 'intelligence', 'os', 'test', 'branches', 'toggles', 'feature', 'programmer',
                    'coding', 'pragprog', 'developer', 'task', 'algorithm', 'algorithms', 'bug', 'bootcamp',
                    'function', 'resume', 'oo', 'design', 'numpy', 'api', 'apis', 'apps', 'dbader_org', 'complexity',
                    'scout', 'boyscout', 'boyscoutrule', 'alexa', 'loop', 'loops', 'thepracticaldev', 'base64',
                    'cryptography', 'developers', 'error', 'class', 'unclebobmartin', 'graph', 'pythonbytes', 'open',
                    'microservice', 'architecture', 'programming', 'nerds', 'martinfowler', 'mfeathers',
                    'containerise', 'iterating', 'filtering', 'language', 'framework', 'platform', 'programmerhumor',
                    'duplication', 'clean', 'coverage', 'commit', 'commits', 'solutions', 'programmers',
                    'cryptographically', 'metric', 'stollcri', 'visualizations', 'git', 'svn', 'bootstrap',
                    'build', 'dom', 'css', 'jquery', 'angular', 'angular2', 'typescript', 'react', 'z3r0_dev',
                    'strftime', 'autostimulation', 'tradeoffs', 'fibonacci', 'markdown', 'editor', 'refactor',
                    'softwaretesting', 'testautomation', 'watir', 'testing', 'cucumber', 'qa', 'pageobject', 'selenium',
                    },
    'leadership': {'leadership', 'lead', 'anyonecanlead', 'davespeck', 'saw', 'apologize', 'managers', 'manage',
                   'growthhacking', 'startup', 'entrepreneur', 'ceo', 'vc', 'positive', 'motivate', 'inspire',
                   'management', 'teams', 'teamwork', 'responsibility', 'context', 'biases', 'heroes', 'leader',
                   'onshift, onshiftgsd', 'onshiftcares', 'onshiftpicnic', 'onshiftengineering', 'innovation',
                   'onshift', 'switch', 'happier', 'talking', 'subtle', 'life', 'opinion', 'advice', 'roi',
                   'inverseconwaymaneuver', 'onshiftgsd', 'livelong', 'zenmonday', 'gsd', 'cultureaced', 'oshackday',
                   'happiness', 'happycows', 'happinessadvantage', 'lifehacks', 'cultural', 'culture',
                   'brain', 'performers', 'joy', 'mentor', 'meetings', 'meeting', 'startups',
                   'journeyman', 'master', 'teammorale', 'ethereum', 'bitcoin', 'windows', 'startupway', 'hfuiym',
                   'bhorowitz', 'audible', 'multitasking', 'overload',
                   'diversity', 'women', 'projectmanagement', 'why', 'simonsinek', 'goldencircle'
                   },
    'agile': {'agile', 'definition', 'ready', 'done', 'experimentation', 'connection', 'doersdecide', 'demo',
              'agile2017', 'experiment', 'continuous', 'collaboration', 'poc', 'mvp', 'slow',
              'scrum', 'waste', 'continuousdelivery', 'flow', 'productbacklogitems', 'transformation', 'person',
              'continuousimprovement', 'everydayagile', 'agileleadership', 'designthinking', 'personas',
              'marches', 'death', 'emergent', 'emergence', 'mob', 'interview', 'safety', 'team',
              'systemsthinking', 'digitaltransformation', 'wip', 'tasktop', 'orgdesign', 'growth', 'kanban',
              'goalsetting', 'process', 'cynefin', 'change', 'autonomy', 'agileaus', 'xp', 'aatc2017', 'scrumban',
              'people', 'disciplinedagile', 'kaizen', 'agilequotes', 'modernagile', 'leanagile', 'outcome', 'lean',
              'value', 'onagile', 'trust', 'mentorship', 'excellence', 'coaching', 'mentoring', 'techcoach',
              'hourofcode', 'craft', 'modern', 'scaling', 'estimation', 'estimate', 'estimates',
              'pairprogramming', 'agilecoach', 'transparency', 'mobprogramming', 'legacycode', 'extremeprogramming',
              'tdd', 'comments', 'safe', 'scrummaster', 'boyscoutrule', 'makingworkvisible',
              'strongstylepairing', 'hypothesis', 'learning', 'reading', 'fail', 'learn', 'docondev',
              'makeyourownlane', 'requirements', 'human', 'organizations', 'red', 'simple', 'craftsman',
              'cleancode', 'cleancoder', 'craftsmanship', 'realgenekim', 'pairing', 'coaches', 'coach',
              'standup', 'future', 'fear', 'slow', 'down', 'speed', 'up', 'cycletime', 'impact', 'waterfall',
              'waterfalls', 'distribution', 'ardita_k', 'mattbarcomb',
              'productmanagement', 'prodmgmt', 'product', 'servicedesign', 'ux', 'cx', 'ui', 'orddesign',
              'productnerd', 'arch', 'productcraft', 'customerfirst', 'design', 'po', 'johncutlefish',
              'agile2018', 'agilealliance'
              },
    # 'diversity': {'diversity', 'women'},
    # 'other': {'valid', 'ideservethis', 'computervision', 'jengacode', 'photo', 'dumb', 'westyaward',
    #           'gameofthrones', 'gobblegobble', 'classic', 'virtual', 'turkishswiftie', 'got', 'friends',
    #           'musiccitycode', 'itsjustnotthathard', 'vogue', 'anger', 'july4th', 'disappointed', 'happythanksgiving',
    #           'laborday', 'successtips', 'cle', 'singer', 'summer', 'sketchnote', 'failure',
    #           'foreverswiftie', 'mha17', 'recommended', 'savethehorsies', 'lego', 'internet'},
}


def get_classification_model(classification_model):
    return classification_model or global_classification_model
