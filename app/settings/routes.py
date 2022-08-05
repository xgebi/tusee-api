import psycopg
from flask import render_template, request, flash, redirect, url_for, current_app, jsonify
from flask_cors import cross_origin

from app.db.db_connection import db_connection
from app.settings import settings
from app.utils.settings_tasks import get_app_settings


@settings.route("/api/app-settings", methods=["GET"])
@cross_origin()
@db_connection
def setup_totp(*args, connection: psycopg.Connection, **kwargs):
	"""


    :param args:
    :param kwargs:
    :return:
    """
	settings = get_app_settings(connection=connection)
	return jsonify(settings)
