import uuid
from typing import Dict

import psycopg


def get_notes_for_user(*args, user_uuid: str, connection: psycopg.Connection, **kwargs):
	with connection.cursor(row_factory=psycopg.rows.dict_row) as cur:
		cur.execute(
			"""SELECT note_uuid, user_uuid, title, note
			FROM tusee_notes WHERE user_uuid = %s;""",
			(user_uuid, )
		)
		temps = cur.fetchall()
		return temps


def get_note_task(*args, user_uuid: str, connection: psycopg.Connection, note_uuid: str, **kwargs):
	with connection.cursor(row_factory=psycopg.rows.dict_row) as cur:
		cur.execute(
			"""SELECT note_uuid, user_uuid, title, note
			FROM tusee_notes WHERE user_uuid = %s AND note_uuid = %s;""",
			(user_uuid, note_uuid)
		)
		temps = cur.fetchone()
		return temps


def create_note_task(*args, user_uuid: str, connection: psycopg.Connection, note: Dict, **kwargs):
	with connection.cursor(row_factory=psycopg.rows.dict_row) as cur:
		cur.execute(
			"""INSERT INTO tusee_notes (note_uuid, user_uuid, title, note) VALUES (%s, %s, %s, %s)
			RETURNING user_uuid, note_uuid, title, note;""",
			(str(uuid.uuid4()), user_uuid, note['title'], note['note'])
		)
		temps = cur.fetchone()
		connection.commit()
		return temps


def update_note_task(*args, user_uuid: str, connection: psycopg.Connection, note: Dict, **kwargs):
	with connection.cursor(row_factory=psycopg.rows.dict_row) as cur:
		cur.execute(
			"""UPDATE tusee_notes SET title = %s, note = %s WHERE user_uuid = %s AND note_uuid = %s
			RETURNING user_uuid, note_uuid, title, note;""",
			(note['title'], note['note'], user_uuid, note['uuid'])
		)
		temps = cur.fetchone()
		connection.commit()
		return temps


def delete_note_task(*args, user_uuid: str, connection: psycopg.Connection, note_uuid: str, **kwargs):
	with connection.cursor(row_factory=psycopg.rows.dict_row) as cur:
		cur.execute(
			"""DELETE FROM tusee_notes WHERE user_uuid = %s AND note_uuid = %s;""",
			(user_uuid, note_uuid)
		)
		connection.commit()
		return True

