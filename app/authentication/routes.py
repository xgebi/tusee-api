import uuid
import psycopg
from flask import render_template, request, flash, redirect, url_for, current_app, jsonify
from flask_cors import cross_origin
import json
from app.authentication.models import User
from argon2 import PasswordHasher

from app.authentication import authentication


@authentication.route("/api/register", methods=["POST"])
@cross_origin()
def register_user(*args, **kwargs):
    """
    Function which will parse JSON to User object

    :param args:
    :param kwargs:
    :return:
    """
    user_json = json.loads(request.data)
    try:
        user = User.create_new(
            user_uuid=str(uuid.uuid4()),
            display_name=user_json.get('displayName'),
            password=user_json.get('password'),
            email=user_json.get('email'),
        )
        user.insert()
        return jsonify({"registrationSuccessful": True})
    except psycopg.Error as e:
        print(e)
        return jsonify({"registrationSuccessful": False, "error": "database"})
    except Exception as e:
        print(e)
        return jsonify({"registrationSuccessful": False, "error": "general"})


@authentication.route("/api/login", methods=["POST"])
@cross_origin()
def login_user(*args, **kwargs):
    """
    Function which will parse JSON to User object

    :param args:
    :param kwargs:
    :return:
    """
    user_json = json.loads(request.data)
    try:
        user = User.get(column='email', value=user_json.get('email'))
        ph = PasswordHasher()
        ph.verify(user.get('password'), user_json.get('password'))
        return jsonify(user)
    except psycopg.Error as e:
        print(e)
        return jsonify({"loginSuccessful": False, "error": "database"})
    except Exception as e:
        print(e)
        return jsonify({"loginSuccessful": False, "error": "general"})


@authentication.route("/api/verify-totp", methods=["POST"])
@cross_origin()
def verify_totp(*args, **kwargs):
    """
    Function which will parse JSON to User object

    :param args:
    :param kwargs:
    :return:
    """
    user_json = json.loads(request.data)
    try:
        user = User(
            user_uuid=str(uuid.uuid4()),
            display_name=user_json.get('displayName'),
            password=user_json.get('password'),
            email=user_json.get('email'),
        )
        user.insert()
        return jsonify({"registrationSuccessful": True})
    except psycopg.Error as e:
        print(e)
        return jsonify({"registrationSuccessful": False, "error": "database"})
    except Exception as e:
        print(e)
        return jsonify({"registrationSuccessful": False, "error": "general"})


@authentication.route("/api/setup-totp", methods=["POST"])
@cross_origin()
def setup_totp(*args, **kwargs):
    """
    Function which will parse JSON to User object

    :param args:
    :param kwargs:
    :return:
    """
    user_json = json.loads(request.data)
    try:
        user = User.get(column='email', value=user_json.get('email'))
        return jsonify(user)
    except psycopg.Error as e:
        print(e)
        return jsonify({"registrationSuccessful": False, "error": "database"})
    except Exception as e:
        print(e)
        return jsonify({"registrationSuccessful": False, "error": "general"})
