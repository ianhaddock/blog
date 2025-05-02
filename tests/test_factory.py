"""test_factor.py"""

from app import create_app


def test_config():
    """test config"""
    assert not create_app().testing
    assert create_app({"TESTING": True}).testing
