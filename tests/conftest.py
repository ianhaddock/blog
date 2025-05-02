""" pytest conftest.py for blog """

import os
import tempfile
import pytest
from app import create_app
from app.db import get_db, init_db


with open(os.path.join(os.path.dirname(__file__), 'data.sql'), 'rb') as f:
    _data_sql = f.read().decode('utf8')


@pytest.fixture
def app():
    # disable redefining outer name - pylint: disable=W0621
    """ build app for tests """
    db_fd, db_path = tempfile.mkstemp()

    app = create_app(
        {
            'TESTING': True,
            'DATABASE': db_path,
            'MARKDOWN_PATH': 'tests/markdown/',
            'SETTINGS_FILE': 'tests/settings.ini'
        }
    )

    with app.app_context():
        init_db()
        get_db().executescript(_data_sql)

    yield app

    os.close(db_fd)
    os.unlink(db_path)


@pytest.fixture
def client(app):
    # disable redefining outer name - pylint: disable=W0621
    """ return test client """
    return app.test_client()


@pytest.fixture
def runner(app):
    # disable redefining outer name - pylint: disable=W0621
    """ return test app runner """
    return app.test_cli_runner()


class AuthActions(object):
    # disable can be removed from bases - pylint: disable=R0205
    # disable redefining outer name - pylint: disable=W0621
    """ auth actions """
    def __init__(self, client):
        self._client = client

    def login(self, username='test', password='test', email='test@example.com'):
        """ login """
        return self._client.post(
                '/auth/login',
                data={'username': username, 'password': password, 'email': email}
                )

    def logout(self):
        """ logout """
        return self._client.get('/auth/logout')


@pytest.fixture
def auth(client):
    # disable redefining outer name - pylint: disable=W0621
    """ return auth client """
    return AuthActions(client)
