import os.path
from flask import Flask
from database import db
from views import view_blueprint


def create_app():
    app_timesheets = Flask(__name__)
    app_timesheets.config['DEBUG'] = True
    app_timesheets.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database/timesheets.db'
    app_timesheets.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.init_app(app_timesheets)
    app_timesheets.register_blueprint(view_blueprint, url_prefix='')
    return app_timesheets


def setup_database(app_timesheets):
    with app_timesheets.app_context():
        db.create_all()


if __name__ == '__main__':
    app = create_app()

    if not os.path.isfile('database/timesheets.db'):
        setup_database(app)

    app.run(app.run(port=5004))
