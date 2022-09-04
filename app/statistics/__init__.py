from flask import Blueprint
statistics = Blueprint('statistics', __name__)
from app.statistics import routes