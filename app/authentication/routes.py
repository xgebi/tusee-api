import datetime
import uuid
import jwt
import psycopg
import pyotp
from flask import render_template, request, flash, redirect, url_for, current_app, jsonify
from flask_cors import cross_origin
import json
from app.authentication.models import User, Key
from argon2 import PasswordHasher, exceptions
from app import db

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
            "board": None
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
        user = User.get(column='email', value=user_json.get('email'))
        user_dict = user.to_dict()
        ph = PasswordHasher()
        result = ph.verify(user_dict.get('password'), user_json.get('password'))
        if result:
            expiry_time = (datetime.datetime.now() + datetime.timedelta(0, 0, 0, 0, 30)).astimezone().isoformat()
            user.expiry_date.set(expiry_time)
            token = jwt.encode({"email": user_dict["email"], "expiry_date": expiry_time},
                               current_app.config["SECRET_KEY"], algorithm="HS256")
            user.token.set(token)
            user.update()

            user_dict["token"] = token
            user_dict["expiry_date"] = expiry_time
            user_dict["password"] = ""
            if not user_dict["uses_totp"] and not user_dict["first_login"]:
                user_dict["keys"] = Key.get_all_dict(column='tusee_user', value=user.user_uuid.value)
            else:
                user_dict["keys"] = []
            return jsonify(user_dict)
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
        user = User({
            "user_uuid": str(uuid.uuid4()),
            "display_name": user_json.get('displayName'),
            "password": user_json.get('password'),
            "email": user_json.get('email'),
        })
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
    user = User.authenticate(request=request)
    if user:
        try:
            totp_data = json.loads(request.data)
            if totp_data["skip"]:
                user.first_login.set(False)
                user.uses_totp.set(False)
                user.update()
                keys = Key.get_all_dict(column="tusee_user", value=user.user_uuid)
                return jsonify({
                        "totpVerified": True,
                        "keys": keys,
                    })
            else:
                totp = pyotp.TOTP(user.totp_secret.value)
                if totp.verify(totp_data["totpCode"]):
                    user.first_login.set(False)
                    user.uses_totp.set(True)
                    user.update()
                    keys = Key.get_all_dict(column="tusee_user", value=user.user_uuid)
                    return jsonify({
                        "totpVerified": True,
                        "keys": keys,
                    })

                return jsonify({
                        "totpVerified": True,
                        "keys": [],
                    }), 401

        except psycopg.Error as e:
            print(e)
            db.con.rollback()
            return jsonify({"registrationSuccessful": False, "error": "database"}), 500
        except Exception as e:
            print(e)
            db.con.rollback()
            return jsonify({"registrationSuccessful": False, "error": "general"}), 500
    return jsonify({"registrationSuccessful": False, "error": "general"}), 500


@authentication.route("/api/authorize-token", methods=["POST"])
@cross_origin()
def setup_totp(*args, **kwargs):
    pass
