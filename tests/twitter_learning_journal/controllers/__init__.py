from flask import Blueprint

from app.twitter_learning_journal.builders.blueprint_builder import build_blueprint


def test_create_blueprint():
    blueprint = build_blueprint('name', 'import_name')

    assert Blueprint == type(blueprint)
    assert 'name' == blueprint.name
    assert 'import_name' == blueprint.import_name
