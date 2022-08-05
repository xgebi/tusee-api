from typing import List

import psycopg

from app.db.db_connection import db_connection


def get_app_settings(*args, connection: psycopg.Connection, **kwargs) -> List or None:
    with connection.cursor(row_factory=psycopg.rows.dict_row) as cur:
        cur.execute("""SELECT settings_name, display_name, settings_value_type, settings_value 
        FROM tusee_settings""")
        temp = cur.fetchall()
        if temp:
            return temp
        return []
