from app.twitter_learning_journal.builders.blueprint_builder import build_blueprint

login_blueprint = build_blueprint('login', __name__)


@login_blueprint.route('/login', methods=['POST'])
def login():
    return 'hello world'
