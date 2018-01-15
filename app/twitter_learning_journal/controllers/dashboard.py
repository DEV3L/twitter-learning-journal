from app.twitter_learning_journal.builders.blueprint_builder import build_blueprint

dashboard_blueprint = build_blueprint('dashboard', __name__)


@dashboard_blueprint.route('/dashboard')
def dashboard():
    return 'hello world'
