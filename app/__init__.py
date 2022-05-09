from flask import Flask
from flask_cors import CORS
from app.db.db import Connector
import os

db = Connector()

def create_app():
    app = Flask(__name__)
    app.config.from_pyfile(os.path.join(os.getcwd(), 'config', f'{os.environ["FLASK_ENV"]}.py'))

    cors = CORS(app)
    db.init_flask(app)

    from app.authentication import authentication
    app.register_blueprint(authentication)

    from app.task import task
    app.register_blueprint(task)

    from app.settings import settings
    app.register_blueprint(settings)

    from app.board import board
    app.register_blueprint(board)

    return app

