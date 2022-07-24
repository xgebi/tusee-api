import datetime
import uuid
import jwt
import psycopg
import pyotp
from flask import render_template, request, flash, redirect, url_for, current_app, jsonify
from flask_cors import cross_origin
import json
from argon2 import PasswordHasher, exceptions
from app import db

from app.authentication import authentication
from app.db.db_connection import db_connection
from app.exceptions import UserExistsException
from app.utils.board_tasks import fetch_available_boards
from app.utils.key_tasks import create_key, get_user_keys
from app.utils.user_tasks import get_user_by_email, update_user, authenticate_user, create_user


@authentication.route("/api/register", methods=["POST"])
@cross_origin()
@db_connection
def register_user(*args, connection: psycopg.Connection, **kwargs):
	"""
	Function which will parse JSON to User object

	:param args:
	:param kwargs:
	:return:
	"""
	user_json = json.loads(request.data)
	try:
		user_uuid = create_user(
			display_name=user_json.get('displayName'),
			password=user_json.get('password'),
			email=user_json.get('email'),
			conn=connection
		)
		create_key(tusee_user=user_uuid, key=user_json.get('key'), conn=connection)
		return jsonify({"registrationSuccessful": True})
	except UserExistsException as e:
		return jsonify({"registrationSuccessful": False, "error": "userExists"}), 403
	except psycopg.Error as e:
		print(e)
		return jsonify({"registrationSuccessful": False, "error": "database"}), 500
	except Exception as e:
		print(e)
		return jsonify({"registrationSuccessful": False, "error": "general"}), 500


@authentication.route("/api/login", methods=["POST"])
@cross_origin()
@db_connection
def login_user(*args, connection: psycopg.Connection, **kwargs):
	"""
	Function which will parse JSON to User object

	:param connection:
	:param args:
	:param kwargs:
	:return:
	"""
	user_json = json.loads(request.data)
	try:
		user = get_user_by_email(email=user_json.get('email'), conn=connection)
		if user is None:
			return jsonify({"loginSuccessful": False, "error": "credentials"}), 403
		ph = PasswordHasher()
		result = ph.verify(user.get('password'), user_json.get('password'))
		if result:
			expiry_time = (datetime.datetime.now() + datetime.timedelta(0, 0, 0, 0, 30)).astimezone().isoformat()
			user["expiry_date"] = expiry_time
			token = jwt.encode({"email": user["email"], "expiry_date": expiry_time},
							   current_app.config["SECRET_KEY"], algorithm="HS256")
			user["token"] = token
			update_user(user, conn=connection)
			user["password"] = ""
			user["totp_secret"] = ""
			if not user["uses_totp"] and not user["first_login"]:
				user["keys"] = get_user_keys(tusee_user=user["user_uuid"], conn=connection)
				user["boards"] = fetch_available_boards(user=user, conn=connection)
			else:
				user["keys"] = []
				user["boards"] = []
			user["loginSuccessful"] = True
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


@authentication.route("/api/totp/verify", methods=["POST"])
@cross_origin()
@db_connection
def verify_totp(*args, connection: psycopg.Connection, **kwargs):
	"""
	Function which will parse JSON to User object

	:param connection:
	:param args:
	:param kwargs:
	:return:
	"""
	user = authenticate_user(request)
	totp_data = json.loads(request.data)
	if user:
		try:
			totp = pyotp.TOTP(user['totp_secret'])
			if totp.verify(totp_data.token):
				keys = get_user_keys(user["user_uuid"], conn=connection)
				boards = fetch_available_boards(user=user, conn=connection)
				return jsonify({"totpVerified": True, "keys": keys, "token": user["token"], "boards": boards})
		except psycopg.Error as e:
			print(e)
			return jsonify({"authenticated": False})
		except Exception as e:
			print(e)
			return jsonify({"authenticated": False})
	return jsonify({"totpVerified": False})


@authentication.route("/api/totp/setup", methods=["POST"])
@cross_origin()
@db_connection
def setup_totp(*args, connection: psycopg.Connection, **kwargs):
	"""
	Function which will parse JSON to User object

	:param connection:
	:param args:
	:param kwargs:
	:return:
	"""
	user = authenticate_user(request, connection=connection)
	if user:
		try:
			totp_data = json.loads(request.data)
			if totp_data["skip"]:
				user["first_login"] = False
				user["uses_totp"] = False
				update_user(user, conn=connection)
				keys = get_user_keys(user["user_uuid"], conn=connection)
				return jsonify({
					"totpVerified": True,
					"keys": keys,
					"token": user["token"]
				})
			else:
				totp = pyotp.TOTP(user["totp_secret"])
				if totp.verify(totp_data["totpCode"]):
					user["first_login"] = False
					user["uses_totp"] = True
					update_user(user)
					keys = get_user_keys(user["user_uuid"], conn=connection)
					return jsonify({
						"token": user["token"],
						"totpVerified": True,
						"keys": keys,
					})

				return jsonify({
					"token": user["token"],
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
