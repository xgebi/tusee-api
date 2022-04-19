from flask import Blueprint
board = Blueprint('board', __name__)
from app.board import routes