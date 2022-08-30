import time
import uuid
from typing import Dict

import psycopg


def get_notes_for_user(*args, user_uuid: str, connection: psycopg.Connection, **kwargs):
	with connection.cursor(row_factory=psycopg.rows.dict_row) as cur:
		cur.execute(
			"""SELECT note_uuid, user_uuid, title, updated
			FROM tusee_notes WHERE user_uuid = %s ORDER BY updated DESC;""",
			(user_uuid, )
		)
		temps = cur.fetchall()
		return temps


def get_note_task(*args, user_uuid: str, connection: psycopg.Connection, note_uuid: str, **kwargs):
	with connection.cursor(row_factory=psycopg.rows.dict_row) as cur:
		cur.execute(
			"""SELECT note_uuid, user_uuid, title, note, created, updated
			FROM tusee_notes WHERE user_uuid = %s AND note_uuid = %s;""",
			(user_uuid, note_uuid)
		)
		temps = cur.fetchone()
		return temps


def create_note_task(*args, user_uuid: str, connection: psycopg.Connection, note: Dict, **kwargs):
	with connection.cursor(row_factory=psycopg.rows.dict_row) as cur:
		cur.execute(
			"""INSERT INTO tusee_notes (note_uuid, user_uuid, title, note, updated, created) 
			VALUES (%s, %s, %s, %s, %s, %s)
			RETURNING user_uuid, note_uuid, title, note, created, updated;""",
			(str(uuid.uuid4()), user_uuid, note['title'], note['note'], time.time() * 1000, time.time() * 1000)
		)
		temps = cur.fetchone()
		connection.commit()
		return temps


def update_note_task(*args, user_uuid: str, connection: psycopg.Connection, note: Dict, **kwargs):
	with connection.cursor(row_factory=psycopg.rows.dict_row) as cur:
		cur.execute(
			"""UPDATE tusee_notes SET title = %s, note = %s, updated = %s WHERE user_uuid = %s AND note_uuid = %s
			RETURNING user_uuid, note_uuid, title, note, created, updated;""",
			(note['title'], note['note'], time.time() * 1000, user_uuid, note['uuid'])
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
		return note_uuid

