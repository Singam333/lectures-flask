from flask import Flask
from flask_cors import CORS

from apis import apis
from models import db

app = Flask(__name__)
CORS(app)

if __name__ == '__main__':
    app.config.from_object('config.Config')

    db.app = app
    db.init_app(app)
    db.create_all()

    app.register_blueprint(apis)

    app.run()
