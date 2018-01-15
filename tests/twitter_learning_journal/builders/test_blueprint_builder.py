from flask import Blueprint

from app.twitter_learning_journal.builders.blueprint_builder import build_blueprint


def test_build_blueprint():
    blueprint = build_blueprint('name', 'import name')

    assert Blueprint == type(blueprint)
    assert 'name' == blueprint.name
    assert 'import name' == blueprint.import_name
