from shorten_url import app, db
from shorten_url.forms import URLForm
from shorten_url.db_models import StoredURL
from flask import render_template, url_for, flash, redirect
import secrets

@app.route('/', methods=['GET', 'POST'])
def home():
    form = URLForm()
    if form.validate_on_submit():
        url = form.url.data
        existing_url = StoredURL.query.filter_by(true_url=url).first()
        if not existing_url:
            key=gen_unique_rand_key()
            stored_url = StoredURL(key=key, true_url=url)
            db.session.add(stored_url)
            db.session.commit()
        else:
            key = existing_url.key
        flash(f'URL shortened to /{key}') # Place domain name in front of '/' when deploying.
        return redirect(url_for('home'))
    return render_template('home.html', form = form)

def gen_unique_rand_key():
    token = secrets.token_urlsafe(6).lower()
    while StoredURL.query.filter_by(key=token).first():
        token = secrets.token_urlsafe(6).lower()
    return token

@app.route('/<string:key>')
def send_to_true_url(key):
    url = StoredURL.query.filter_by(key=key).first()
    if url:
        url.visits += 1
        db.session.commit()
        return redirect(url.true_url)
    return redirect(url_for('home'))

@app.route('/analytics/<string:key>')
def analytics(key):
    url = StoredURL.query.filter_by(key=key).first()
    if url:
        return render_template('analytics.html', url_data=url)
    return redirect(url_for('home'))