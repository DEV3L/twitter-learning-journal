import os
import tempfile
import unittest

from app.twitter_learning_journal.database.sqlalchemy_database import build_tables, Database
from server import app


class FlaskrTestCase(unittest.TestCase):
    def setUp(self):
        self.db_fd, app.config['DATABASE'] = tempfile.mkstemp()
        app.testing = True

        self.app = app.test_client()
        self.database = Database()

        with app.app_context():
            build_tables(self.database)

    def tearDown(self):
        os.close(self.db_fd)
        os.unlink(app.config['DATABASE'])

    def test_login_endpoint_exists(self):
        expected_response_code = 200
        username = 'username'
        password = 'password'

        response = self.app.post('/login', data=dict(
            username=username,
            password=password
        ), follow_redirects=True)

        assert expected_response_code == response.status_code
