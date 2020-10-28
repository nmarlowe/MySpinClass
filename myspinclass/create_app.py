from flask import Flask

def create_app():
    app = Flask(__name__)

    # Init the db. I'd like to have SQLAlchemy

    # We should use alembic for SQLAlchemy.


    return app