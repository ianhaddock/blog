"""__init__.py"""

import os
from configparser import ConfigParser
from flask import Flask
from flaskext.markdown import Markdown


# Disable import outside toplevel warning - pylint: disable=C0415
def create_app(test_config=None):
    """create and configure the app"""
    app = Flask(__name__, static_folder="static", instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY="dev",
        DATABASE=os.path.join(app.instance_path, "blogapp.sqlite"),
    )

    # set to allow markdown filter in templates
    Markdown(app, extensions=["fenced_code", "codehilite"], safe_mode=True)

    if test_config is None:
        # load config when not testing
        app.config.from_pyfile("config.py", silent=True)

    else:
        # load test config
        app.config.from_mapping(test_config)

    # instance folder try
    try:
        os.makedirs(app.instance_path, exist_ok=True)
    except OSError as err:
        raise Exception(f"Can't write to instance path: {err}")

    # import or create settings file
    settings = ConfigParser()
    app.config.settings_file = os.path.join(app.instance_path, "settings.ini")
    if not os.path.exists(app.config.settings_file):
        # base settings file
        settings["settings"] = {
            "blog_name": "blog.example.com",
            "contact_email": "test@example.com",
            "usericon_mouseover_enable": "True",
            "usericon": "custom/usericon-dark-48px.png",
            "usericon_mouseover": "custom/usericon-light-48px.png",
            "favicon": "custom/favicon.ico",
            "github_url": "https://github.com",
            "linkedin_url": "https://www.linkedin.com",
            "register": "False",
            "markdown_path": "custom/markdown/",
            "panoramic_path": "custom/pano/",
            "use_copy_date_start": "false",
            "copy_date_start": 2024,
            "copy_date_end": 2024,
        }
        settings["admin_reset"] = {
            "username": "account_name_to_reset",
            "password": "new_account_password",
        }
        with open(app.config.settings_file, "w", encoding="utf-8") as f:
            settings.write(f)

    settings.read(app.config.settings_file)

    # add settings to flask config dict
    setting = settings["settings"]

    for key, value in setting.items():
        if key == "register":
            app.config["register"] = setting.getboolean("register")
        elif key == "use_copy_date_start":
            app.config["use_copy_date_start"] = setting.getboolean(
                "use_copy_date_start"
            )
        elif key == "usericon_mouseover_enable":
            mouseover_enable_status = settings["settings"].getboolean(
                "usericon_mouseover_enable"
            )
            app.config["usericon_mouseover_enable"] = mouseover_enable_status
        else:
            app.config[key] = value

    # back to imports
    from . import db

    db.init_app(app)

    from . import auth

    app.register_blueprint(auth.bp)

    from . import blog

    app.register_blueprint(blog.bp)
    app.add_url_rule("/", endpoint="index")

    from . import settings

    app.register_blueprint(settings.bp)

    return app
