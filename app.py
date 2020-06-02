from flask import Flask
from models import db

app = Flask(__name__)

if __name__ == '__main__':
    app.config.from_object('config.Config')

    db.app = app
    db.init_app(app)
    db.create_all()

    app.run()
