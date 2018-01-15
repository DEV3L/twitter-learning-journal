from flask import Blueprint


def build_blueprint(name, import_name):
    return Blueprint(name, import_name, template_folder='templates')
