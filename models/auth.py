from . import db


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)
    city = db.Column(db.String(100), nullable=False)
    college = db.Column(db.String(100), nullable=False)
    degree = db.Column(db.String(100), nullable=False)
    stream = db.Column(db.String(100), nullable=False)
    grad_year = db.Column(db.String(100), nullable=False)
    job = db.Column(db.String(100), nullable=False)
