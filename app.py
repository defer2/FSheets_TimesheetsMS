import os.path
from flask import Flask
from database import db
from views import view_blueprint
from flask_cors import CORS


def create_app():
    app_timesheets = Flask(__name__)
    app_timesheets.config['DEBUG'] = True
    app_timesheets.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database/timesheets.db'
    app_timesheets.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app_timesheets.config['CORS_HEADERS'] = 'Content-Type'
    db.init_app(app_timesheets)
    app_timesheets.register_blueprint(view_blueprint, url_prefix='')
    return app_timesheets


def setup_database(app_timesheets):
    with app_timesheets.app_context():
        db.create_all()


app = create_app()
cors = CORS(app)

if __name__ == '__main__':
    if not os.path.isfile('database/timesheets.db'):
        setup_database(app)

    app.run(host='0.0.0.0', port=5012)

