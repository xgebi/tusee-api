from flask import current_app, wrappers
from datetime import datetime
from typing import Dict
from argon2 import PasswordHasher
import pyotp
import jwt

from app.db.model import Model
from app.db.column import Column


class User(Model):
    __table_name__ = 'tusee_users'

    user_uuid = Column(str, primary_key=True)
    display_name = Column(str, default="Human")
    password = Column(str, nullable=False)
    email = Column(str, nullable=False)
    expiry_date = Column(type(datetime), default=datetime.utcnow())
    first_login = Column(bool, nullable=False, default=True)
    uses_totp = Column(bool, nullable=False, default=False)
    totp_secret = Column(str)
    token = Column(str, default='')

    @classmethod
    def create_new(cls, user_uuid, display_name, password, email):
        ph = PasswordHasher()
        return cls({
            "display_name": display_name,
            "user_uuid": user_uuid,
            "password": ph.hash(password),
            "email": email,
            "totp_secret": pyotp.random_base32()
        })

    def __init__(self, user: Dict):
        super().__init__(user)
        self.user_uuid.set(user.get('user_uuid'))
        self.display_name.set(user.get('display_name'))
        self.password.set(user.get('password'))
        self.email.set(user.get('email'))
        self.expiry_date.set(user.get('expiry_date'))
        self.first_login.set(user.get('first_login'))
        self.uses_totp.set(user.get('uses_totp'))
        self.totp_secret.set(user.get('totp_secret'))
        self.token.set(user.get('token'))

    @staticmethod
    def authenticate(request: wrappers.Request):
        auth = request.headers.get('authorization').split(" ")
        decoded = jwt.decode(auth[1], current_app.config["SECRET_KEY"], algorithms="HS256")
        user = User.get(column="email", value=decoded["email"])
        if user.expiry_date == datetime.fromisoformat(decoded["expiry_date"]) and user.expiry_date > datetime.now():
            return user
        return None


class Key(Model):
    __table_name__ = 'tusee_encrypted_keys'

    key_uuid = Column(str, primary_key=True)
    tusee_user = Column(str, nullable=False)
    key = Column(str, nullable=False)
    boardless = Column(str, nullable=False)

    def __init__(self, key: Dict):
        super().__init__(key)
        self.key_uuid.set(key.get('key_uuid'))
        self.tusee_user.set(key.get('tusee_user'))
        self.key.set(key.get('key'))
        self.boardless.set(key.get('boardless'))
