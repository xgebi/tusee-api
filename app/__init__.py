from flask import Flask
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
import os

db = SQLAlchemy()


def create_app():
    app = Flask(__name__)
    cors = CORS(app)
    db.init_app(app)

    app.config.from_pyfile(os.path.join(os.getcwd(), 'config', f'{os.environ["FLASK_ENV"]}.py'))

    from app.authentication import authentication
    app.register_blueprint(authentication)

    return app

