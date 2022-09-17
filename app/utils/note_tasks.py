import time
import uuid
from datetime import datetime
from typing import Dict

import psycopg


def get_notes_for_user(*args, user_uuid: str, connection: psycopg.Connection, **kwargs):
	with connection.cursor(row_factory=psycopg.rows.dict_row) as cur:
		cur.execute(
			"""SELECT note_uuid, user_uuid, title,
			(EXTRACT (EPOCH FROM updated) * 1000)::bigint AS updated
			FROM tusee_notes WHERE user_uuid = %s ORDER BY updated DESC;""",
			(user_uuid, )
		)
		notes = cur.fetchall()
		return notes


def get_note_task(*args, user_uuid: str, connection: psycopg.Connection, note_uuid: str, **kwargs):
	with connection.cursor(row_factory=psycopg.rows.dict_row) as cur:
		cur.execute(
			"""SELECT note_uuid, user_uuid, title, note,
			(EXTRACT (EPOCH FROM created) * 1000)::bigint AS created,
			(EXTRACT (EPOCH FROM updated) * 1000)::bigint AS updated
			FROM tusee_notes WHERE user_uuid = %s AND note_uuid = %s;""",
			(user_uuid, note_uuid)
		)
		temp = cur.fetchone()
		return temp


def create_note_task(*args, user_uuid: str, connection: psycopg.Connection, note: Dict, **kwargs):
	with connection.cursor(row_factory=psycopg.rows.dict_row) as cur:
		cur.execute(
			"""INSERT INTO tusee_notes (note_uuid, user_uuid, title, note, updated, created) 
			VALUES (%s, %s, %s, %s, %s, %s)
			RETURNING note_uuid, user_uuid, title, note, created, updated;""",
			(str(uuid.uuid4()), user_uuid, note['title'], note['note'], datetime.now(), datetime.now())
		)
		temps = cur.fetchone()
		connection.commit()
		return temps


def update_note_task(*args, user_uuid: str, connection: psycopg.Connection, note: Dict, **kwargs):
	with connection.cursor(row_factory=psycopg.rows.dict_row) as cur:
		cur.execute(
			"""UPDATE tusee_notes SET title = %s, note = %s, updated = %s WHERE user_uuid = %s AND note_uuid = %s
			RETURNING user_uuid, note_uuid, title, note, (EXTRACT (EPOCH FROM created) * 1000)::bigint AS created,
			(EXTRACT (EPOCH FROM updated) * 1000)::bigint AS updated""",
			(note['title'], note['note'], datetime.now(), user_uuid, note['note_uuid'])
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

