from flask import render_template, request, flash, redirect, url_for, current_app, jsonify
from flask_cors import cross_origin

from app.settings import settings
from app.utils.settings_tasks import get_app_settings


@settings.route("/api/app-settings", methods=["GET"])
@cross_origin()
def setup_totp(*args, **kwargs):
    """


    :param args:
    :param kwargs:
    :return:
    """
    return jsonify(get_app_settings())