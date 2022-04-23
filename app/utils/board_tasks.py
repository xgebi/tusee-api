import uuid
from datetime import datetime, timezone, timedelta
from typing import List, Dict

from flask import jsonify
from psycopg import Cursor

from app import db
from app.utils.audit_log_tasks import log_permission_violation
from app.utils.key_tasks import create_key


def fetch_board(board_uuid, user):
    conn = db.get_connection()
    with conn.cursor() as cur:
        cur.execute("""SELECT tusee_user FROM tusee_encrypted_keys WHERE board = %s""",
                    (board_uuid,))
        temp = cur.fetchall()
        if temp is None:
            log_permission_violation(
                cur=cur,
                user_uuid=user['user_uuid'],
                event=f"Attempted to update non-existent board {board_uuid} by {user['user_uuid']}"
            )
            return {}

        cur.execute("""SELECT board_uuid, name, description, owner, created, columns FROM tusee_boards 
                WHERE board_uuid = %s""",
                    (board_uuid,))
        temp = cur.fetchone()

        return board_to_dict(temp)


def fetch_available_boards(user):
    conn = db.get_connection()
    with conn.cursor() as cur:
        cur.execute("""SELECT board_uuid, name, description, owner, created, columns FROM tusee_boards 
        WHERE board_uuid IN (SELECT board FROM tusee_encrypted_keys WHERE tusee_user = %s AND board IS NOT NULL)""",
                    (user['user_uuid'],))
        temp = cur.fetchall()
        if len(temp) > 0:
            return [board_to_dict(item) for item in temp]
        return []


def create_board(user, board_data):
    board = board_data.get('board')
    conn = db.get_connection()
    with conn.cursor() as cur:
        board_uuid = str(uuid.uuid4())

        cur.execute(
            """INSERT INTO tusee_boards
            (board_uuid, name, description, owner, created, columns) 
            VALUES (%s, %s, %s, %s, %s, %s)
            RETURNING board_uuid, name, description, owner, created, columns""",
            (board_uuid, board.get('name'), board.get('description'), user["user_uuid"], datetime.now(),
             board.get('columns')))
        temp = cur.fetchone()
        task_dict = board_to_dict(temp)
    conn.commit()
    key = create_key(tusee_user=user["user_uuid"], key=board_data.get("key").get("key"), board=board_uuid)
    return jsonify({"token": user["token"], "board": task_dict, "key": key}), 200


def update_board(board, user):
    conn = db.get_connection()
    with conn.cursor() as cur:
        cur.execute(
            """SELECT board_uuid, name, description, owner, created, columns
            FROM tusee_boards WHERE board_uuid = %s""",
            (board['boardUuid'], )
        )
        temp = cur.fetchone()
        if temp is None:
            log_permission_violation(
                cur=cur,
                user_uuid=user['user_uuid'],
                event=f"Attempted to update non-existent board {board['boardUuid']} by {user['user_uuid']}"
            )
            return jsonify({}), 403

        board_dict = board_to_dict(temp)

        cur.execute("""SELECT tusee_user FROM tusee_encrypted_keys WHERE board = %s""",
                    (board_dict.get('boardUuid'),))
        temp = cur.fetchall()
        if len(temp) > 0:
            return jsonify({"token": user["token"], "board": update_board_db(cur=cur, board=board)}), 200
        log_permission_violation(
            cur=cur,
            user_uuid=user['user_uuid'],
            event=f"Attempted to update board {board['boardUuid']} by {user['user_uuid']}"
        )
        return jsonify({}), 403


def delete_board(board_uuid, user):
    conn = db.get_connection()
    with conn.cursor() as cur:
        cur.execute(
            """SELECT board_uuid, name, description, owner, created, columns
            FROM tusee_boards WHERE board_uuid = %s""",
            (board_uuid,)
        )
        temp = cur.fetchone()
        if temp is None:
            log_permission_violation(
                cur=cur,
                user_uuid=user['user_uuid'],
                event=f"Attempted to update non-existent board {board_uuid} by {user['user_uuid']}"
            )
            return jsonify({}), 403

        cur.execute("""SELECT tusee_user FROM tusee_encrypted_keys WHERE board = %s""",
                    (board_uuid,))
        temp = cur.fetchall()
        if len(temp) > 0:
            return jsonify({
                "token": user['token'],
                "task": delete_board_db(cur, board_uuid=board_uuid)
            })
        log_permission_violation(
            cur=cur,
            user_uuid=user['user_uuid'],
            event=f"Attempted to delete {board_uuid} by {user['user_uuid']}"
        )
        return jsonify({}), 500


def board_to_dict(temp: List) -> Dict:
    return {
        "boardUuid": temp[0],
        "name": temp[1],
        "description": temp[2],
        "owner": temp[3],
        "created": temp[4],
        "columns": temp[5]
    }


def update_board_db(cur: Cursor, board: Dict):
    cur.execute(
        """UPDATE tusee_boards 
        SET name = %s, owner = %s, columns = %s, description = %s
        WHERE board_uuid = %s
        RETURNING board_uuid, name, description, owner, created, columns""",
        (board.get("name"), board.get("owner"), board.get("columns"), board.get("description"),
         board.get("boardUuid")))
    temp = cur.fetchone()
    cur.connection.commit()
    return board_to_dict(temp)


def delete_board_db(cur: Cursor, board_uuid: str):
    cur.execute(
        """DELETE FROM tusee_encrypted_keys WHERE board = %s""",
        (board_uuid,))
    cur.execute(
        """DELETE FROM tusee_boards WHERE board_uuid = %s""",
        (board_uuid, ))
    cur.connection.commit()
    return board_uuid
