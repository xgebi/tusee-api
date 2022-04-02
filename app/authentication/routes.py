import uuid
import psycopg
from flask import render_template, request, flash, redirect, url_for, current_app, jsonify
from flask_cors import cross_origin
import json
from app.authentication.models import User, Key
from argon2 import PasswordHasher, exceptions

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
        key = Key({
            "key_uuid": str(uuid.uuid4()),
            "tusee_user": user.user_uuid.value,
            "key": user_json.get('key'),
            "boardless": True
        })
        key.insert()
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
        user = User.get(column='email', value=user_json.get('email'), to_dict=True)
        ph = PasswordHasher()
        result = ph.verify(user.get('password'), user_json.get('password'))
        if result:
            del user["password"]
            return jsonify(user)
    except exceptions.InvalidHash as e:
        print(e)
        return jsonify({"loginSuccessful": False, "error": "credentials"}), 403
    except psycopg.Error as e:
        print(e)
        return jsonify({"loginSuccessful": False, "error": "database"}), 500
    except Exception as e:
        print(e)
        return jsonify({"loginSuccessful": False, "error": "general"}), 500


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
