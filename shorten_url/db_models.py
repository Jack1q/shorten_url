from shorten_url import db

class StoredURL(db.Model):
    key = db.Column(db.String, unique=True, primary_key=True, nullable=False)
    true_url = db.Column(db.String, unique=True, nullable=False)
    visits = db.Column(db.Integer, default=0)