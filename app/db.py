"""blog db.py"""

import sqlite3
import click
from flask import current_app, g


def get_db():
    """return existing or create new sqlite db"""
    if "db" not in g:
        g.db = sqlite3.connect(
            current_app.config["DATABASE"], detect_types=sqlite3.PARSE_DECLTYPES
        )
        g.db.row_factory = sqlite3.Row

    return g.db


def close_db(e=None):
    """close existing db"""
    db = g.pop("db", e)

    if db is not None:
        db.close()


def init_db():
    """init a new db instance"""
    db = get_db()

    with current_app.open_resource("schema.sql") as f:
        db.executescript(f.read().decode("utf8"))


@click.command("init-db")
def init_db_command():
    """clear data and create new tables"""
    init_db()
    click.echo("Initialized the database.")


def init_app(app):
    """init a new app instance"""
    app.teardown_appcontext(close_db)
    app.cli.add_command(init_db_command)


def load_db(path="markdown/*.md"):
    """placeholder: load content from markdown files"""
    print(path)


def get_user_ids():
    """return user ids from db"""
    db = get_db()
    return db.execute("SELECT ID FROM USER;").fetchall()


def get_titles():
    """pulls title information for the right side bar"""

    table = (
        get_db()
        .execute(
            "SELECT p.id, title, created, author_id, username"
            " FROM post p JOIN user u ON p.author_id = u.id"
            " ORDER BY created DESC"
        )
        .fetchall()
    )

    return table


def reorder_posts():
    """create tmp table with null ids and insert posts to reorder"""
    db = get_db()
    db.execute(
        "CREATE TEMPORARY TABLE tmp AS SELECT * FROM post ORDER BY"
        " datetime(created) ASC"
    )
    db.execute("UPDATE tmp SET id = NULL")
    db.execute("DROP TABLE post")
    db.execute(
        "CREATE TABLE post ("
        " id INTEGER PRIMARY KEY AUTOINCREMENT,"
        " author_id INTEGER NOT NULL,"
        " created TIMESTAMP UNIQUE NOT NULL DEFAULT CURRENT_TIMESTAMP,"
        " title TEXT NOT NULL,"
        " body TEXT NOT NULL,"
        " FOREIGN KEY (author_id) REFERENCES user (id)"
        " );"
    )
    db.execute("INSERT INTO post SELECT * FROM tmp")
    db.execute("DROP TABLE tmp")
    db.commit()


def drop_posts():
    """reset posts table"""
    db = get_db()
    db.execute("DROP TABLE post")
    db.execute(
        "CREATE TABLE post ("
        " id INTEGER PRIMARY KEY AUTOINCREMENT,"
        " author_id INTEGER NOT NULL,"
        " created TIMESTAMP UNIQUE NOT NULL DEFAULT CURRENT_TIMESTAMP,"
        " title TEXT NOT NULL,"
        " body TEXT NOT NULL,"
        " FOREIGN KEY (author_id) REFERENCES user (id)"
        " );"
    )
    db.commit()
