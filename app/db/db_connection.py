from typing import Optional
from flask import current_app
from functools import wraps
import psycopg


def db_connection(fn):
	"""
	Decorator function which creates a connection to database for the function

	:param fn:
	:return:
	"""

	@wraps(fn)
	def wrapper(*args, connection: Optional[psycopg.Connection] = None, **kwargs):
		if connection is not None:
			return fn(*args, connection=connection, **kwargs)
		conn = connect_to_db()
		return fn(*args, connection=conn, **kwargs)

	return wrapper


def connect_to_db() -> Optional[psycopg.Connection]:
	"""
	creates a connection to database

	:return:
	"""
	config = current_app.config
	conn_str = f"{config['DATABASE_STRING']}"
	try:
		return psycopg.connect(conn_str)
	except psycopg.errors.DatabaseError:
		return None
