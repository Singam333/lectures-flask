from . import db


class Video(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    key = db.Column(db.String(30), unique=True, nullable=False)
    name = db.Column(db.String(30), nullable=False)
    user = db.relationship('User', backref='videos', lazy=True)
