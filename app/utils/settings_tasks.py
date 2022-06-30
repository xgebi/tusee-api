from typing import List

import psycopg

from app import db


def get_app_settings() -> List or None:
    conn = db.get_connection()
    with conn.cursor(row_factory=psycopg.rows.dict_row) as cur:
        cur.execute("""SELECT settings_name, display_name, settings_value_type, settings_value 
        FROM tusee_settings""")
        temp = cur.fetchall()
        if temp:
            return temp
        return None
