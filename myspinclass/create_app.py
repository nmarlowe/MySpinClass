from flask import Flask

def create_app():
    app = Flask(__name__)

    from myspinclass.app import bluetooth_endpoints
    app.register_blueprint(bluetooth_endpoints.ble_bp)
    # Init the db. I'd like to have SQLAlchemy

    # We should use alembic for SQLAlchemy.


    return app



