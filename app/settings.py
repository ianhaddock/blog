from flask import Blueprint, current_app as app
from configparser import ConfigParser
from werkzeug.security import generate_password_hash
from app.db import get_db
import os

bp = Blueprint('settings', __name__)


def account_reset(settings):
    """update password if existing username is set in settings.ini"""

    passw = settings.get('admin_reset', 'password')
    uname = settings.get('admin_reset', 'username')

    hashed_passw = generate_password_hash(passw)
    settings.set('admin_reset', 'password', hashed_passw)

    db = get_db()
    db.execute(
        "UPDATE user SET password = ? WHERE username = ?",
        (hashed_passw, uname)
        )
    db.commit()

    set_settings(settings)

    return None


def get_settings(settings_file='instance/settings.ini'):
    """store blog settings if exists, create if not"""

    settings = ConfigParser()
    settings.read(os.path.join(app.instance_path, 'settings.ini'))

    # check if password reset is set
    pw = settings.get('admin_reset', 'password')
    if not len(pw) == 102 \
            and not pw == 'new_account_password':
        account_reset(settings)

    # add settings section to global flask config
    setting = settings['settings']

    for key, value in setting.items():
        app.config[key] = value
    app.config['register'] = setting.getboolean('register')

    return settings


def set_settings(settings, settings_file='instance/settings.ini'):
    """write all to the settings file"""

    with open(os.path.join(app.instance_path, 'settings.ini'), 'w') as setting:
        settings.write(setting)
