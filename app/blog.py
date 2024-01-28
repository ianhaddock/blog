# blog site
# used palletsprojects.com flask tutorial
# started Nov 2022

from flask import (
        Blueprint, flash, g, redirect, render_template, request, url_for
        )
from werkzeug.exceptions import abort
from app.auth import login_required
from app.db import (
        get_db, reorder_posts, drop_posts, load_db, get_user_ids, get_titles,
        insert_demo_post
        )
from datetime import datetime
from flask import current_app as app
import glob
import yaml
import os
from app.settings import pano, set_settings, get_settings

bp = Blueprint('blog', __name__)


@bp.route('/')
@bp.route('/<int:id>')
def index(id=None):
    """presents newest post in long form, the next most recent suggested
    below, with a list of all posts on the right"""

    titles = get_titles()
    count = len(titles)

    # if new install, show register page instead of index
    user_count = len(get_user_ids())
    if user_count == 0:
        app.config['register'] = True
        return redirect(url_for('auth.register'))

    # generate welcome post if post count is zero or markdown folder is empty
    if len(titles) == 0:
        insert_demo_post()
        return redirect(url_for('blog.index'))

    # show latest post if id is invalid
    if not id or id > count:
        id = count

    next_id = id - 1

    # suggest most recent post below post 1
    if id == 1:
        next_id = count

    posts = get_posts(id, next_id, False)

    # show only the demo post if this is a new install
    if posts == 1:
        next_p = 1
    else:
        next_p = posts[-1]
    # truncate next post body at third '.' and add elipse
    next_post = '.'.join(next_p['body'].split('.')[:3])+('...')

    return render_template('blog/index.html', posts=posts,
                           next_post=next_post, titles=titles,
                           pano=pano())


@bp.route('/create', methods=('GET', 'POST'))
@login_required
def create():
    if request.method == 'POST':
        title = request.form['title']
        body = request.form['body']
        error = None

        if not title:
            error = 'Title is required.'

        if error is not None:
            flash(error)
        else:
            db = get_db()
            db.execute(
                    'INSERT INTO post (title, body, author_id)'
                    ' VALUES (?, ?, ?)', (title, body, g.user['id'])
                    )
            db.commit()

            return redirect(url_for('blog.index'))

    return render_template('blog/create.html', pano=pano())


def get_posts(id, next_id, check_author=True):
    """get the main and secondary post for index page"""

    # if viewing the first post, show the most recent as the suggested
    if id == 1:
        posts = get_db().execute(
                'SELECT p.id, title, body, created, author_id, username'
                ' FROM post p JOIN user u ON p.author_id = u.id'
                ' WHERE p.id = ? OR p.id = ?'
                ' ORDER BY created ASC', (next_id, id)
                ).fetchall()

    else:
        posts = get_db().execute(
                'SELECT p.id, title, body, created, author_id, username'
                ' FROM post p JOIN user u ON p.author_id = u.id'
                ' WHERE p.id = ? OR p.id = ?'
                ' ORDER BY created DESC', (next_id, id)
                ).fetchall()

    return (posts)


def get_post(id, check_author=True):
    """get a single post for editing"""
    post = get_db().execute(
            'SELECT p.id, title, body, created, author_id, username'
            ' FROM post p JOIN user u ON p.author_id = u.id'
            ' WHERE p.id = ?', (id,)
            ).fetchone()

    if post is None:
        abort(404, f"Post id {id} does not exist.")

    if check_author and post['author_id'] != g.user['id']:
        abort(403)

    return (post)


@bp.route('/<int:id>/update', methods=('GET', 'POST'))
@login_required
def update(id):
    post = get_post(id)

    if request.method == 'POST':
        title = request.form['title']
        body = request.form['body']
        error = None

        if not title:
            error = 'Title is required.'

        if error is not None:
            flash(error)
        else:
            db = get_db()
            db.execute(
                'UPDATE post SET title = ?, body = ? WHERE id = ?',
                (title, body, id)
                )
            db.commit()
            return redirect(url_for('blog.index', id=id))

    return render_template('blog/update.html', post=post, pano=pano())


@bp.route('/<int:id>/delete', methods=('POST',))
@login_required
def delete(id):
    get_post(id)
    db = get_db()
    db.execute('DELETE FROM post WHERE id = ?', (id,))
    db.commit()
    reorder_posts()
    return redirect(url_for('blog.index'))


@bp.route('/settings', methods=('GET', 'POST'))
@login_required
def settings():
    """load and edit settings in config.py file"""

    settings = get_settings()
    setting = settings['settings']

    if request.method == 'POST':
        setting['blog_name'] = request.form['blogname']
        setting['contact_email'] = request.form['contactemail']
        setting['usericon'] = request.form['usericon']
        setting['usericon_mouseover'] = request.form['usericon_mouseover']
        setting['usericon_mouseover_enable'] = request.form['usericon_mouseover_enable']
        setting['favicon'] = request.form['favicon']
        setting['github_url'] = request.form['githuburl']
        setting['linkedin_url'] = request.form['linkedinurl']
        setting['register'] = request.form['register']
        setting['markdown_path'] = request.form['markdownpath']
        setting['panoramic_path'] = request.form['panoramics']
        setting['use_copy_date_start'] = request.form['use_copy_date_start']
        setting['copy_date_start'] = request.form['copy_date_start']
        setting['copy_date_end'] = request.form['copy_date_end']

        set_settings(settings)

        error = None
            # error tests
        if error is None:
            get_settings()
            return redirect(url_for("blog.index"))

        flash(error, 'error')

    return render_template('blog/settings.html', pano=pano())


@bp.route('/reload')
@login_required
def reload_markdown():
    """Loads markdown files from a directory and adds or updates existing posts
    in the db"""

    path = "app/static/" + app.config['markdown_path']
    file_list = []

    if not os.path.exists(path):
        flash(path + ' not found', 'error')
        return redirect(url_for('blog.index'))

    # this should be
    load_db(path)

    drop_posts()

    for file in glob.glob(path + '*.md'):
        with open(file, 'r', encoding='utf-8') as theFile:
            content = theFile.read()

            try:
                tags, content = content.split('---\n')
                tags = yaml.safe_load(tags)

            except Exception as error:
                flash(file + ': ' + str(error), 'error')
                tags = []
                content = ''

            else:
                if 'author_id' not in tags:
                    tags['author_id'] = 1
                if 'date' in tags:
                    if isinstance(tags['date'], datetime):
                        tags['created'] = tags['date']

                file_list.append(file)
                db = get_db()

                try:
                    db.execute(
                        'INSERT INTO post (title, body, author_id, created)'
                        ' VALUES (?, ?, ?, ?)'
                        ' ON CONFLICT(created) DO UPDATE'
                        '  SET title = EXCLUDED.title,'
                        '  body = EXCLUDED.body,'
                        '  created = EXCLUDED.created',
                        (tags['title'], content, tags['author_id'],
                         tags['created'])
                        )

                except Exception as error:
                    flash(file + ': missing ' + str(error), 'error')

                else:
                    db.commit()
                    flash('Loaded: ' + file, 'info')

    reorder_posts()

    return redirect(url_for('blog.index'))
