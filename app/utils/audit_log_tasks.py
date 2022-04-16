import uuid
from datetime import datetime

from psycopg import Cursor
from flask import request


def log_permission_violation(cur: Cursor, user_uuid: str, event: str):
    ip = request.environ.get('HTTP_X_FORWARDED_FOR', request.remote_addr)
    cur.execute("""INSERT INTO tusee_permissions_audit_log (entry_uuid, tusee_user, timedate, ip, event) 
    VALUES (%s, %s, %s, %s, %s)""",
                (str(uuid.uuid4()), user_uuid, datetime.now(), ip, event))
    cur.connection.commit()


def log_access(cur: Cursor, user_uuid: str, event: str):
    ip = request.environ.get('HTTP_X_FORWARDED_FOR', request.remote_addr)
    cur.execute("""INSERT INTO tusee_access_audit_log (entry_uuid, tusee_user, timedate, ip, event) 
    VALUES (%s, %s, %s, %s, %s)""",
                (str(uuid.uuid4()), user_uuid, datetime.now(), ip, event))
    cur.connection.commit()
