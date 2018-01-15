from flask import Blueprint

from app.twitter_learning_journal.controllers.dashboard import dashboard


def test_dashboard_blueprint():
    from app.twitter_learning_journal.controllers.dashboard import dashboard_blueprint

    assert dashboard_blueprint
    assert 'dashboard' == dashboard_blueprint.name
    assert 'app.twitter_learning_journal.controllers.dashboard' == dashboard_blueprint.import_name
    assert Blueprint == dashboard_blueprint.__class__


def test_dashboard():
    assert 'hello world' == dashboard()
