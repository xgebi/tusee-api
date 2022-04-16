import datetime
import uuid
from typing import Dict, List

from app import db


def create_key(tusee_user: str, key: str, board: str = None) -> Dict:
    key_dict = None
    conn = db.get_connection()
    with conn.cursor() as cur:
        key_uuid = str(uuid.uuid4())
        cur.execute(
            """INSERT INTO tusee_encrypted_keys (key_uuid, tusee_user, key, board) VALUES (%s, %s, %s, %s)
            RETURNING key_uuid, key, board""",
            (key_uuid, tusee_user, key, board))
        temp = cur.fetchone()
        key_dict = {
            "key_uuid": key_uuid,
            "tusee_user": temp[0],
            "key": temp[1],
            "board": temp[2]
        }
    conn.commit()
    return key_dict


def get_user_keys(tusee_user: str) -> List:
    keys = []
    conn = db.get_connection()
    with conn.cursor() as cur:
        cur.execute(
            """SELECT key_uuid, tusee_user, key, board FROM tusee_encrypted_keys WHERE tusee_user = %s""",
            (tusee_user,))
        temp = cur.fetchall()
        keys = [
            {
                "key_uuid": item[0],
                "tusee_user": item[1],
                "key": item[2],
                "board": item[3]
            } for item in temp
        ]
    return keys
