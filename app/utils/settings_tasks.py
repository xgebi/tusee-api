from typing import List
from app import db


def get_app_settings() -> List or None:
    conn = db.get_connection()
    with conn.cursor() as cur:
        cur.execute("""SELECT settings_name, display_name, settings_value_type, settings_value 
        FROM tusee_settings""")
        temp = cur.fetchall()
        if temp:
            return [{
                "settingsName": item[0],
                "displayName": item[2],
                "settingsValueType": item[2],
                "settingsValue": item[3],
            } for item in temp]
        return None
