from typing import List

import psycopg

from app.db.db_connection import db_connection


@db_connection
def get_app_settings(conn: psycopg.Connection) -> List or None:
    with conn.cursor(row_factory=psycopg.rows.dict_row) as cur:
        cur.execute("""SELECT settings_name, display_name, settings_value_type, settings_value 
        FROM tusee_settings""")
        temp = cur.fetchall()
        if temp:
            return temp
        return None
