import time
import uuid
from datetime import datetime
from typing import Dict

import psycopg


def get_all_goals_for_user(*args, user_uuid: str, connection: psycopg.Connection, **kwargs):
	with connection.cursor(row_factory=psycopg.rows.dict_row) as cur:
		cur.execute(
			"""SELECT goal_uuid, user_uuid, goal, target_date, added_date, done_date, done
			FROM tusee_goals WHERE user_uuid = %s ORDER BY target_date DESC NULLS LAST, added_date DESC;""",
			(user_uuid,)
		)
		temps = cur.fetchall()
		return temps


def get_goals_for_user_doneness(*args, user_uuid: str, doneness: bool, connection: psycopg.Connection, **kwargs):
	with connection.cursor(row_factory=psycopg.rows.dict_row) as cur:
		cur.execute(
			"""SELECT goal_uuid, user_uuid, goal, target_date, added_date, done_date, done
			FROM tusee_goals WHERE user_uuid = %s AND done = %s ORDER BY target_date DESC NULLS LAST, added_date DESC;""",
			(user_uuid, doneness)
		)
		temps = cur.fetchall()
		return temps


def get_goal_task(*args, user_uuid: str, connection: psycopg.Connection, goal_uuid: str, **kwargs):
	with connection.cursor(row_factory=psycopg.rows.dict_row) as cur:
		cur.execute(
			"""SELECT goal_uuid, user_uuid, goal, target_date, added_date, done_date, done
			FROM tusee_goals WHERE user_uuid = %s AND goal_uuid = %s;""",
			(user_uuid, goal_uuid)
		)
		temps = cur.fetchone()
		return temps


def create_goal_task(*args, user_uuid: str, connection: psycopg.Connection, goal: Dict, **kwargs):
	with connection.cursor(row_factory=psycopg.rows.dict_row) as cur:
		cur.execute(
			"""INSERT INTO tusee_goals (goal_uuid, user_uuid, goal, target_date, added_date, done_date, done) 
			VALUES (%s, %s, %s, %s, %s, %s, %s)
			RETURNING goal_uuid, user_uuid, goal, target_date, added_date, done_date, done""",
			(str(uuid.uuid4()), user_uuid, goal['goal'], goal['target'], datetime.now(), None, False)
		)
		temps = cur.fetchone()
		connection.commit()
		return temps


def update_goal_task(*args, user_uuid: str, connection: psycopg.Connection, goal: Dict, **kwargs):
	with connection.cursor(row_factory=psycopg.rows.dict_row) as cur:
		cur.execute(
			"""UPDATE tusee_goals SET goal = %s, target_date = %s, done_date = %s, done = %s 
			WHERE user_uuid = %s AND goal_uuid = %s
			RETURNING goal_uuid, user_uuid, goal, target_date, added_date, done_date, done""",
			(goal['goal'], goal['target'], datetime.now() if goal['done'] else None, goal['done'],
			user_uuid, goal['goal_uuid'])
		)
		temps = cur.fetchone()
		connection.commit()

		return temps


def delete_goal_task(*args, user_uuid: str, connection: psycopg.Connection, goal_uuid: str, **kwargs):
	with connection.cursor(row_factory=psycopg.rows.dict_row) as cur:
		cur.execute(
			"""DELETE FROM tusee_goals WHERE user_uuid = %s AND goal_uuid = %s;""",
			(user_uuid, goal_uuid)
		)
		connection.commit()
		return goal_uuid
