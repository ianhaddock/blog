"""test_blog.py"""

import pytest
from app.db import get_db


def test_index(client, auth, app):
    """test index"""
    response = client.get("/")
    assert b"Login" in response.data
    assert b"Register" in response.data

    auth.login()
    response = client.get("/")
    assert b"Logout" in response.data
    assert b"Reload" in response.data
    assert b"New" in response.data
    assert b'/update"' in response.data
    assert b"test title" in response.data
    assert b"2018-01-01" in response.data
    assert b"test\nbody" in response.data

    app.config["REGISTER"] = False
    response = client.get("/")
    assert b"Register" not in response.data


def test_index_entry_2(client):  # , auth):
    """test blog entry 1"""
    response = client.get("/1")
    assert b"test title 2" in response.data


def test_index_bad_id(client):  # , auth):
    """test bad blog entry id"""
    assert client.get("/999").status_code == 200


@pytest.mark.parametrize(
    "path",
    (
        "/create",
        "/1/update",
        "/1/delete",
    ),
)
def test_login_required(client, path):
    """test login required"""
    response = client.post(path)
    assert response.headers["Location"] == "/auth/login"


def test_author_required(app, client, auth):
    """test author required"""
    # change the post auth to a different user
    with app.app_context():
        db = get_db()
        db.execute("UPDATE post SET author_id = 2 WHERE id = 1")
        db.commit()

    auth.login()
    # current user should not be able to modify other users post
    assert client.post("/1/update").status_code == 403
    assert client.post("/1/delete").status_code == 403

    # current user does not see edit button
    assert b'href="/1/update"' not in client.get("/").data


@pytest.mark.parametrize(
    "path",
    (
        "/3/update",
        "/3/delete",
    ),
)
def test_exists_required(client, auth, path):
    """test auth for existing paths only"""
    auth.login()
    assert client.post(path).status_code == 404


def test_markdown_reload(client, auth):  # app, auth):
    """test reload markdown"""
    auth.login()
    result = client.get("/reload", follow_redirects=False)
    assert result.status_code == 302
    assert result.location == "/"


def test_markdown_path(client, app, auth):
    """test markdown path is valid"""
    auth.login()
    app.config["MARKDOWN_PATH"] = "app/no_folder/"
    result = client.get("/reload", follow_redirects=False)
    assert result.status_code == 302
    assert result.location == "/"


def test_create(client, auth, app):
    """test create blog entry"""
    auth.login()
    assert client.get("/create").status_code == 200
    client.post("/create", data={"title": "created", "body": ""})

    with app.app_context():
        db = get_db()
        count = db.execute("SELECT COUNT(id) FROM post").fetchone()[0]
        assert count == 3


def test_update(client, auth, app):
    """test blog entry update"""
    auth.login()
    assert client.get("/1/update").status_code == 200
    client.post("/1/update", data={"title": "updated", "body": ""})

    with app.app_context():
        db = get_db()
        post = db.execute("SELECT * FROM post WHERE id = 1").fetchone()
        assert post["title"] == "updated"


@pytest.mark.parametrize(
    "path",
    (
        "/create",
        "/1/update",
    ),
)
def test_create_update_validate(client, auth, path):
    """test blog entry update is valid"""
    auth.login()
    response = client.post(path, data={"title": "", "body": ""})
    assert b"Title is required." in response.data


def test_delete(client, auth, app):
    """test blog entry delete"""
    auth.login()
    response = client.post("/1/delete")
    assert response.headers["Location"] == "/"

    with app.app_context():
        db = get_db()
        post = db.execute("SELECT * FROM post WHERE id = 1").fetchone()
        assert "test title 2" in post["title"]
