from app import db
from app.db.column import Column
from typing import Dict


class Model:
    __table_name__ = None

    def __init__(self, item: Dict):
        self.item = item

    @classmethod
    def get(cls, column: str or None = None, value=None, to_dict=False) -> 'Model' or Dict:
        keys = [key for key in vars(cls) if not key.startswith('_') and type(cls.__getattribute__(cls, key)) == Column]
        if column in keys and value is not None:
            columns = ",".join(keys)
            query = f"SELECT {columns} FROM {cls.__table_name__} WHERE {column} = %s"
            with db.con.cursor() as cur:
                cur.execute(query, (value,))
                res = cur.fetchone()
                result_dict = {}
                for i in range(len(keys)):
                    result_dict[keys[i]] = res[i]
                if to_dict:
                    return result_dict
                return cls(result_dict)
        return cls

    def get_all(self):
        pass

    def insert(self):
        keys = [key for key in dir(self) if type(self.__getattribute__(key)) == Column]
        columns = ",".join(keys)
        stand_ins = ",".join(["%s" for key in keys])
        values = [self.__getattribute__(key).value for key in keys]
        query = f"INSERT INTO {self.__table_name__} ({columns}) VALUES ({stand_ins})"
        with db.con.cursor() as cur:
            cur.execute(query, values)
            db.con.commit()

    def update(self):
        keys = [key for key in dir(self) if type(self.__getattribute__(key)) == Column]
        primary_key = None
        for key in keys:
            if self.__getattribute__(key).primary_key:
                primary_key = key
        if primary_key is None:
            return
        keys = [key for key in keys if key != primary_key]
        columns = " = %s".join(keys)
        values = [self.__getattribute__(key).value for key in keys]
        values.append(self.__getattribute__(primary_key).value)
        query = f"UPDATE {self.__table_name__} SET {columns} WHERE {primary_key} = %s;"
        with db.con.cursor() as cur:
            cur.execute(query, values)
            db.con.commit()

    def delete(self, column: str = '', value: str = ''):
        key = [key for key in dir(self) if type(self.__getattribute__(key)) == Column and self.__getattribute__(key).primary_key][0]
        values = (self.__getattribute__(key).value, )
        query = f"DELETE FROM {self.__table_name__} WHERE {key} = %s;"
        with db.con.cursor() as cur:
            cur.execute(query, values)
            db.con.commit()
