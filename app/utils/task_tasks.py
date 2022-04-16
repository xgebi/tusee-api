import uuid
from datetime import datetime
from typing import List

from app import db


def get_standalone_tasks_for_user(user_uuid: str) -> List:
    conn = db.get_connection()
    with conn.cursor() as cur:
        cur.execute(
            """SELECT task_uuid, creator, board, description, updated, created FROM tusee_tasks WHERE creator = %s 
            AND board = %s""",
            (user_uuid, None)
        )
        temps = cur.fetchall()
        return [{
            "task_uuid": temp[0],
            "creator": temp[1],
            "board": temp[2],
            "description": temp[3],
            "updated": temp[4],
            "created": temp[5]
        } for temp in temps]


def get_tasks_for_board(board_uuid, user_uuid):
    conn = db.get_connection()
    with conn.cursor() as cur:
        cur.execute("""SELECT board FROM tusee_encrypted_keys WHERE board = %s AND tusee_user = %s""",
                    (board_uuid, user_uuid))
        temp = cur.fetchall()
        if len(temp) == 0:
            raise Exception("Cannot access tasks for this board")
        cur.execute(
            """SELECT task_uuid, creator, board, description, updated, created FROM tusee_tasks WHERE creator = %s 
            AND board = %s""",
            (board_uuid, )
        )
        temps = cur.fetchall()
        return [{
            "task_uuid": temp[0],
            "creator": temp[1],
            "board": temp[2],
            "description": temp[3],
            "updated": temp[4],
            "created": temp[5]
        } for temp in temps]


def create_task(user_uuid, board_uuid, title, description,):
    task_dict = None
    conn = db.get_connection()
    with conn.cursor() as cur:
        task_uuid = str(uuid.uuid4())
        cur.execute(
            """INSERT INTO tusee_tasks (task_uuid, creator, board, title, description, updated, created) VALUES (%s, %s, %s, %s, %s, %s)
            RETURNING title, description, creator, updated, created, board""",
            (task_uuid, user_uuid, board_uuid, title, description, datetime.now(), datetime.now()))
        temp = cur.fetchone()
        task_dict = {
            "task_uuid": task_uuid,
            "title": temp[0],
            "description": temp[1],
            "creator": temp[2],
            "updated": temp[3],
            "created": temp[4],
            "board": temp[5]
        }
    conn.commit()
    return task_dict


def update_task():
    pass


def delete_task():
    pass
