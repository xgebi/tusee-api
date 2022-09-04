from flask import Blueprint
goal = Blueprint('goal', __name__)
from app.goal import routes