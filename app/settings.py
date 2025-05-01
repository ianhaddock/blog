""" blog settings.py """

import os
import random
from configparser import ConfigParser
from flask import Blueprint, flash, current_app as app
from werkzeug.security import generate_password_hash
from app.db import get_db


bp = Blueprint('settings', __name__)


def pano():
    """select random page header panorama image"""
    custom_path = "app/static/" + app.config['panoramic_path']
    the_pano = random.choice(os.listdir(custom_path))
    return app.config['panoramic_path'] + the_pano


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


def get_settings(settings_file='settings.ini'):
    """store blog settings if exists, create if not"""

    settings = ConfigParser()
    settings.read(os.path.join(app.instance_path, settings_file))

    # check if password reset is set
    pw = settings.get('admin_reset', 'password')
    if not len(pw) == 102 \
            and pw != 'new_account_password':
        account_reset(settings)

    return settings


def set_settings(settings, settings_file='settings.ini'):
    """write all to the settings file"""

    setting = settings['settings']
    error = False

    for key, value in setting.items():
        if key == 'register':
            try:
                app.config['register'] = settings['settings'].getboolean('register')
            except ValueError as err:
                flash('Enable Register must be True or False: ' + str(err), 'error')
                error = True

        elif key == 'user_copy_date_start':
            use_copy_date = settings['settings'].getboolean('use_copy_date_start')
            try:
                app.config['use_copy_date_start'] = use_copy_date
            except ValueError as err:
                flash('Use Copyright Start Date must be True or False: ' + str(err), 'error')
                error = True

        elif key == 'usericon_mouseover_enable':
            mouseover_enable_status = settings['settings'].getboolean('usericon_mouseover_enable')
            try:
                app.config['usericon_mouseover_enable'] = mouseover_enable_status
            except ValueError as err:
                flash('User Icon Mouseover must be True or False:' + str(err), 'error')
                error = True
        else:
            app.config[key] = value

    if error is True:
        return

    with open(os.path.join(app.instance_path, settings_file), 'w', encoding='utf-8') as setting:
        settings.write(setting)
