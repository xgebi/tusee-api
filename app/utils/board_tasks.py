import uuid
from datetime import datetime, timezone, timedelta
from typing import List, Dict

from flask import jsonify
from psycopg import Cursor

from app import db
from app.utils.audit_log_tasks import log_permission_violation


def create_board(user, board):
    task_dict = None
    conn = db.get_connection()
    with conn.cursor() as cur:
        board_uuid = str(uuid.uuid4())

        cur.execute(
            """INSERT INTO tusee_boards
            (board_uuid, name, description, owner, created, columns) 
            VALUES (%s, %s, %s, %s, %s, %s)
            RETURNING board_uuid, name, description, owner, created, columns""",
            (board_uuid, board.get('name'), board.get('description'), user["userUuid"], datetime.now(),
             board.get('columns')))
        temp = cur.fetchone()
        task_dict = board_to_dict(temp)
    conn.commit()
    return jsonify({"token": user["token"], "board": task_dict}), 200


def update_board(task, user):
    conn = db.get_connection()
    with conn.cursor() as cur:
        cur.execute(
            """SELECT task_uuid, creator, board, title, description, updated, created, deadline, start_time, task_status
            FROM tusee_tasks WHERE task_uuid = %s""",
            (task['task_uuid'], )
        )
        temp = cur.fetchone()
        if temp is None:
            log_permission_violation(
                cur=cur,
                user_uuid=user['user_uuid'],
                event=f"Attempted to update non-existent task {task['task_uuid']} by {user['user_uuid']}"
            )
            return jsonify({}), 403

        task_dict = board_to_dict(temp)

        if task.get('board'):
            cur.execute("""SELECT tusee_user FROM tusee_encrypted_keys WHERE board = %s""",
                        (task_dict.get('board'),))
            temp = cur.fetchall()
            if len(temp) > 0:
                return jsonify({"token": user["token"], "task": update_task_db(cur=cur, task=task)}), 200
            log_permission_violation(
                cur=cur,
                user_uuid=user['user_uuid'],
                event=f"Attempted to update task {task['task_uuid']} on board {task.get('board')} by {user['user_uuid']}"
            )
            return jsonify({}), 403
        else:
            if task_dict.get("creator") == user['user_uuid']:
                return jsonify({"token": user["token"], "task": update_task_db(cur=cur, task=task)}), 200
            log_permission_violation(
                cur=cur,
                user_uuid=user['user_uuid'],
                event=f"Attempted to update task {task['task_uuid']} by {user['user_uuid']}"
            )
            return jsonify({}), 403


def delete_board(task_uuid, user):
    conn = db.get_connection()
    with conn.cursor() as cur:
        cur.execute(
            """SELECT task_uuid, creator, board, title, description, updated, created, deadline, start_time, task_status
            FROM tusee_tasks WHERE task_uuid = %s""",
            (task_uuid,)
        )
        temp = cur.fetchone()
        if temp is None:
            log_permission_violation(
                cur=cur,
                user_uuid=user['user_uuid'],
                event=f"Attempted to update non-existent task {task_uuid} by {user['user_uuid']}"
            )
            return jsonify({}), 403

        task_dict = board_to_dict(temp)

        if task_dict.get('board'):
            cur.execute("""SELECT tusee_user FROM tusee_encrypted_keys WHERE board = %s""",
                        (task_dict.get('board'),))
            temp = cur.fetchall()
            if len(temp) > 0:
                return jsonify({
                    "token": user['token'],
                    "task": delete_task_db(cur, task_uuid=task_uuid)
                })
            log_permission_violation(
                cur=cur,
                user_uuid=user['user_uuid'],
                event=f"Attempted to update task {task_uuid} on board {task_dict.get('board')} by {user['user_uuid']}"
            )
            return jsonify({}), 403
        else:
            if task_dict.get("creator") == user['user_uuid']:
                return jsonify({
                    "token": user['token'],
                    "task": delete_task_db(cur, task_uuid=task_uuid)
                })
            log_permission_violation(
                cur=cur,
                user_uuid=user['user_uuid'],
                event=f"Attempted to update task {task_uuid} by {user['user_uuid']}"
            )
            return jsonify({}), 403


def board_to_dict(temp: List) -> Dict:
    return {
        "board_uuid": temp[0],
        "name": temp[1],
        "description": temp[2],
        "owner": temp[3],
        "created": temp[4],
        "columns": temp[5]
    }


def update_board_db(cur: Cursor, task: Dict):
    cur.execute(
        """UPDATE tusee_tasks 
        SET creator = %s, board = %s, title = %s, description = %s, updated = %s, deadline = %s, start_time = %s,
        task_status = %s
        WHERE task_uuid = %s
        RETURNING task_uuid, creator, board, title, description, updated, created, deadline, start_time, task_status""",
        (task.get("creator"), task.get("board_uuid"), task.get("title"), task.get("description"), datetime.now(),
         task.get("deadline"), task.get("start_time"), task.get("task_status"), task.get("task_uuid")))
    temp = cur.fetchone()
    cur.connection.commit()
    return board_to_dict(temp)


def delete_board_db(cur: Cursor, task_uuid: str):
    cur.execute(
        """DELETE FROM tusee_tasks WHERE task_uuid = %s""",
        (task_uuid, ))
    return task_uuid
