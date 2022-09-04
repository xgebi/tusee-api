import time
import uuid
from datetime import datetime
from typing import Dict

import psycopg


def get_events_for_user(*args, user_uuid: str, connection: psycopg.Connection, **kwargs):
	with connection.cursor(row_factory=psycopg.rows.dict_row) as cur:
		cur.execute(
			"""SELECT event_uuid, user_uuid, event_name, start_timedate, end_timedate
			FROM tusee_events WHERE user_uuid = %s ORDER BY start_timedate DESC;""",
			(user_uuid, )
		)
		temps = cur.fetchall()
		return temps


def get_event_task(*args, user_uuid: str, connection: psycopg.Connection, event_uuid: str, **kwargs):
	with connection.cursor(row_factory=psycopg.rows.dict_row) as cur:
		cur.execute(
			"""SELECT event_uuid, user_uuid, event_name, description, start_timedate, end_timedate
			FROM tusee_events WHERE user_uuid = %s AND event_uuid = %s;""",
			(user_uuid, event_uuid)
		)
		temps = cur.fetchone()
		return temps


def create_event_task(*args, user_uuid: str, connection: psycopg.Connection, event: Dict, **kwargs):
	with connection.cursor(row_factory=psycopg.rows.dict_row) as cur:
		cur.execute(
			"""INSERT INTO tusee_events (event_uuid, user_uuid, event_name, description, start_timedate, end_timedate) 
			VALUES (%s, %s, %s, %s, %s, %s)
			RETURNING event_uuid, user_uuid, event_name, start_timedate, end_timedate;""",
			(str(uuid.uuid4()), user_uuid, event['name'], event['description'], event['start'], event['end'])
		)
		temps = cur.fetchone()
		connection.commit()
		return temps


def update_event_task(*args, user_uuid: str, connection: psycopg.Connection, event: Dict, **kwargs):
	with connection.cursor(row_factory=psycopg.rows.dict_row) as cur:
		cur.execute(
			"""UPDATE tusee_events SET event_name = %s, description = %s, start_timedate = %s, end_timedate = %s 
			WHERE user_uuid = %s AND event_uuid = %s
			RETURNING event_uuid, user_uuid, event_name, start_timedate, end_timedate;""",
			(event['name'], event['description'], event['start'], event['end'], user_uuid, event['event_uuid'])
		)
		temps = cur.fetchone()
		connection.commit()

		return temps


def delete_event_task(*args, user_uuid: str, connection: psycopg.Connection, event_uuid: str, **kwargs):
	with connection.cursor(row_factory=psycopg.rows.dict_row) as cur:
		cur.execute(
			"""DELETE FROM tusee_events WHERE user_uuid = %s AND event_uuid = %s;""",
			(user_uuid, event_uuid)
		)
		connection.commit()
		return event_uuid

