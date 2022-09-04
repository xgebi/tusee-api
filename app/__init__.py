from flask import Flask
from flask_cors import CORS
import os

def create_app():
    app = Flask(__name__)
    app.config.from_pyfile(os.path.join(os.getcwd(), 'config', f'{os.environ["FLASK_ENV"]}.py'))

    cors = CORS(app)

    from app.authentication import authentication
    app.register_blueprint(authentication)

    from app.task import task
    app.register_blueprint(task)

    from app.note import note
    app.register_blueprint(note)

    from app.settings import settings
    app.register_blueprint(settings)

    from app.board import board
    app.register_blueprint(board)

    from app.event import event
    app.register_blueprint(event)

    from app.goal import goal
    app.register_blueprint(goal)

    from app.statistics import statistics
    app.register_blueprint(statistics)

    return app

