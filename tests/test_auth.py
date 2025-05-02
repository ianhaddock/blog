""" test_auth.py """

import pytest
from flask import g, session
from app.db import get_db


def test_register(client, app):
    """ test user registration """
    assert client.get('/auth/register').status_code == 200

    response = client.post(
            '/auth/register', data={'username': 'a', 'password': 'a',
                                    'email': 'a@example.com'}
            )
    assert response.headers['Location'] == '/auth/login'

    with app.app_context():
        assert get_db().execute(
                "SELECT * FROM user WHERE username = 'a'",
                ).fetchone() is not None


def test_register_off(client, app):
    """ test disable registration """
    app.config['register'] = False
    assert client.get('/auth/register').status_code == 302


@pytest.mark.parametrize(('username', 'password', 'email', 'message'), (
    ('', '', 'test@test.com', b'Username is required.'),
    ('a', '', 'test@test.com', b'Password is required.'),
    ('a', 'a', '', b'Email is required.'),
    ('test', 'test', 'test@example.com', b'already registered'),
    ))
def test_register_validate_input(client, username, password, email, message):
    """ test registration is valid """
    response = client.post(
            '/auth/register',
            data={'username': username, 'password': password, 'email': email}
            )
    assert message in response.data


def test_login(client, auth):
    """ test login is valid """
    assert client.get('/auth/login').status_code == 200
    response = auth.login()
    assert response.headers["Location"] == "/"

    with client:
        client.get('/')
        assert session['user_id'] == 1
        assert g.user['username'] == 'test'


@pytest.mark.parametrize(('username', 'password', 'message'), (
    ('a', 'test', b'Incorrect username or password.'),
    ('test', 'a', b'Incorrect username or password.'),
    ))
def test_login_validate_input(auth, username, password, message):
    """ test login validate input """
    response = auth.login(username, password)
    assert message in response.data


def test_logout(client, auth):
    """ test logout """
    auth.login()

    with client:
        auth.logout()
        assert 'user_id' not in session
