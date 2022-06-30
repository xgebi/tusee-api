import datetime
import uuid
from typing import Dict, List

import psycopg

from app import db


def create_key(tusee_user: str, key: str, conn: psycopg.Connection, board: str = None) -> Dict:
    with conn.cursor(row_factory=psycopg.rows.dict_row) as cur:
        key_uuid = str(uuid.uuid4())
        cur.execute(
            """INSERT INTO tusee_encrypted_keys (key_uuid, tusee_user, key, board) VALUES (%s, %s, %s, %s)
            RETURNING key_uuid, key, board""",
            (key_uuid, tusee_user, key, board))
        key_dict = cur.fetchone()
    conn.commit()
    return key_dict


def get_user_keys(tusee_user: str, conn: psycopg.Connection) -> List:
    keys = []
    with conn.cursor(row_factory=psycopg.rows.dict_row) as cur:
        cur.execute(
            """SELECT key_uuid, tusee_user, key, board FROM tusee_encrypted_keys WHERE tusee_user = %s""",
            (tusee_user,))
        keys = cur.fetchall()
    return keys
