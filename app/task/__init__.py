from flask import Blueprint
task = Blueprint('task', __name__)
from app.task import routes