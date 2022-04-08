from flask import render_template, request, flash, redirect, url_for, current_app
from flask_cors import cross_origin

from app.authentication.models import User
from app.event import event


@event.route("/api/events", methods=["GET"])
@cross_origin()
def setup_totp(*args, **kwargs):
    """


    :param args:
    :param kwargs:
    :return:
    """
    user = User.authenticate(request=request)


@event.route("/api/event/<id>", methods=["GET", "POST", "PUT"])
@cross_origin()
def setup_totp(*args, id: str, **kwargs):
    """


    :param args:
    :param id:
    :param kwargs:
    :return:
    """
    user = User.authenticate(request=request)