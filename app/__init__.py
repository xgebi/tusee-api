from flask import Flask
from flask_cors import CORS
from app.db.db import Connector
from flask_sqlalchemy import SQLAlchemy
import os

db = Connector()

def create_app():
    app = Flask(__name__)
    app.config.from_pyfile(os.path.join(os.getcwd(), 'config', f'{os.environ["FLASK_ENV"]}.py'))

    cors = CORS(app)
    db.init_flask(app)

    from app.authentication import authentication
    app.register_blueprint(authentication)

    return app

