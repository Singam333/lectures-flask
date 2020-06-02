from os import environ, path
from dotenv import load_dotenv

basedir = path.abspath(path.dirname(__file__))
load_dotenv(path.join(basedir, ".env"))


class Config:
    # Database
    SQLALCHEMY_DATABASE_URI = "mysql://{}:{}@{}/{}".format(
        environ.get("MYSQL_USER"),
        environ.get("MYSQL_PASSWORD"),
        environ.get("MYSQL_HOST"),
        environ.get("MYSQL_DB"),
    )

    FLASK_ENV = "development"
    DEBUG = True

    # Secrets
    SECRET_KEY = environ.get("SECRET_KEY")
