from app import db
from app.db.column import Column

class Model:
    __table_name__ = None

    @classmethod
    def get(cls, column: str or None = None, value=None) -> 'Model':
        if column in vars(cls).keys():
            print(value)
            pass
        return cls

    def get_all(self):
        pass

    def insert(self):
        keys = [key for key in dir(self) if not key.startswith('_') and type(self.__getattribute__(key)) == Column]
        columns = ",".join(keys)
        stand_ins = ",".join(["%s" for key in keys])
        values = [self.__getattribute__(key).value for key in keys]
        query = f"INSERT INTO {self.__table_name__} ({columns}) VALUES ({stand_ins})"
        with db.con.cursor() as cur:
            cur.execute(query, values)
            db.con.commit()

    def update(self):
        pass

    def delete(self):
        pass
