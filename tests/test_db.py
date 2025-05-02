"""test_db.py"""

import sqlite3
import pytest
from app.db import get_db


class Recorder(object):
    # disable too few public methods - pylint: disable=R0903
    # disable can be removed from bases - pylint: disable=R0205
    """docstring"""
    called = False


def test_get_close_db(app):
    """get close db"""
    with app.app_context():
        db = get_db()
        assert db is get_db()

    with pytest.raises(sqlite3.ProgrammingError) as e:
        db.execute("SELECT 1")

    assert "closed" in str(e.value)


def test_init_db_command(runner, monkeypatch):
    """init db"""

    def fake_init_db():
        Recorder.called = True

    monkeypatch.setattr("app.db.init_db", fake_init_db)
    result = runner.invoke(args=["init-db"])
    assert "Initialized" in result.output
    assert Recorder.called
