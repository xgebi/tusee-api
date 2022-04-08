from datetime import datetime
from typing import Dict

from app.db.column import Column
from app.db.model import Model


class Task(Model):
    __table_name__ = 'tusee_tasks'

    task_uuid = Column(str, primary_key=True)
    creator = Column(str, nullable=False)
    board = Column(str, nullable=True)
    description = Column(str, nullable=True)
    created = Column(type(datetime), default=datetime.utcnow())
    updated = Column(type(datetime), default=datetime.utcnow())

    def __init__(self, key: Dict):
        super().__init__(key)
        self.task_uuid.set(key.get('key_uuid'))
        self.creator.set(key.get('tusee_user'))
        self.board.set(key.get('board'))
        self.description.set(key.get('description'))
        self.created.set(key.get('created'))
        self.updated.set(key.get('updated'))
