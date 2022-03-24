from datetime import datetime

from app import db
from sqlalchemy.dialects import postgresql


class User(db.Model):
    __tablename__ = 'book'

    user_uuid = db.Column(postgresql.VARCHAR(200), primary_key=True)
    display_name = db.Column(postgresql.TEXT, default="Human")
    password = db.Column(postgresql.VARCHAR(500), nullable=False, default="Human")
    email = db.Column(postgresql.VARCHAR(350), nullable=False, unique=True)
    expiry_date = db.Column(postgresql.DATE, default=datetime.utcnow())
    first_login = db.Column(postgresql.BOOLEAN, nullable=False, default=True)
    uses_totp = db.Column(postgresql.BOOLEAN, nullable=False, default=False)

    def __init__(self, user_uuid, display_name, password, email):
        self.user_uuid = user_uuid
        self.display_name = display_name
        self.password = password
        self.email = email
