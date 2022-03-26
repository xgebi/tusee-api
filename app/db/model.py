from app import db
from app.db.column import Column
from typing import Dict


class Model:
    __table_name__ = None

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
