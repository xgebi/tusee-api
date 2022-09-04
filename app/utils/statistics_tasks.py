import time
import uuid
from datetime import datetime
from typing import Dict

import psycopg


def get_statistics_for_user(*args, user_uuid: str, connection: psycopg.Connection, **kwargs):
	with connection.cursor(row_factory=psycopg.rows.dict_row) as cur:
		cur.execute(
			"""SELECT stat_uuid, user_uuid, stat_name, stat_value, recorded_at, stat_type, note
			FROM tusee_statistics WHERE user_uuid = %s ORDER BY recorded_at DESC;""",
			(user_uuid, )
		)
		temps = cur.fetchall()
		return temps


def get_statistics_entry_task(*args, user_uuid: str, connection: psycopg.Connection, stat_uuid: str, **kwargs):
	with connection.cursor(row_factory=psycopg.rows.dict_row) as cur:
		cur.execute(
			"""SELECT stat_uuid, user_uuid, stat_name, stat_value, recorded_at, stat_type, note
			FROM tusee_statistics WHERE user_uuid = %s AND stat_uuid = %s;""",
			(user_uuid, stat_uuid)
		)
		temps = cur.fetchone()
		return temps


def create_statistics_entry_task(*args, user_uuid: str, connection: psycopg.Connection, stat: Dict, **kwargs):
	with connection.cursor(row_factory=psycopg.rows.dict_row) as cur:
		cur.execute(
			"""INSERT INTO tusee_statistics
			(stat_uuid, user_uuid, stat_name, stat_value, recorded_at, updated_at, stat_type, note) 
			VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
			RETURNING stat_uuid, user_uuid, stat_name, stat_value, recorded_at, stat_type, note;""",
			(str(uuid.uuid4()), user_uuid, stat['name'], stat['value'], datetime.now(), datetime.now(), stat['type'],
			stat['note'])
		)
		temps = cur.fetchone()
		connection.commit()
		return temps


def update_statistics_entry_task(*args, user_uuid: str, connection: psycopg.Connection, stat: Dict, **kwargs):
	with connection.cursor(row_factory=psycopg.rows.dict_row) as cur:
		cur.execute(
			"""UPDATE tusee_statistics SET stat_name = %s, stat_value = %s, note = %s, stat_type = %s, updated_at = %s 
			WHERE user_uuid = %s AND stat_uuid = %s
			RETURNING stat_uuid, user_uuid, stat_name, stat_value, recorded_at, stat_type, note""",
			(stat['name'], stat['value'], stat['note'], stat['type'], datetime.now(), user_uuid, stat['stat_uuid'])
		)
		temps = cur.fetchone()
		connection.commit()

		return temps


def delete_statistics_entry_task(*args, user_uuid: str, connection: psycopg.Connection, stat_uuid: str, **kwargs):
	with connection.cursor(row_factory=psycopg.rows.dict_row) as cur:
		cur.execute(
			"""DELETE FROM tusee_statistics WHERE user_uuid = %s AND stat_uuid = %s;""",
			(user_uuid, stat_uuid)
		)
		connection.commit()
		return stat_uuid

