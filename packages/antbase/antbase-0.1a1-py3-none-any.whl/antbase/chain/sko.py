from datetime import datetime
from antbase  import Db

from __future__ import annotations

class Sko:
    def __init__(self, _sko, _key, source, body=None):
        self._sko   = _sko
        self._key   = _key
        self.body   = body
        self.source = source

        if   source == 'load':     self.load()
        elif source == 'create':   self.create()
        elif source == 'recreate': self.recreate()
        elif source == 'next':     self.next()

    def load(self):
        """Загрузка данных из MongoDB"""
        data = Db.find_one("Sko", self._sko, {"_key": self._key})
        if data: self.__dict__.update(data)
        else: raise Exception(f"Объект с ключом {self._key} не найден.")
        return self

    def save(self):
        """Сохранение объекта в MongoDB"""
        self._modified = datetime.now()
        Db.update_one("Sko", self._sko, {"_key": self._key}, {"$set": self.__dict__}, upsert=True)
        return self

    def remove(self):
        """Удаление объекта из MongoDB"""
        Db.delete_one("Sko", self._sko, {"_key": self._key})
        return self

    def create(self):
        """Создание нового объекта"""
        if Db.find_one("Sko", self._sko, {"_key": self._key}):
            raise Exception(f"Объект с ключом {self._key} уже существует.")
        self._created = datetime.now()
        self._modified = datetime.now()
        Db.insert_one("Sko", self._sko, self.__dict__)
        return self

    def recreate(self):
        """Пересоздание объекта"""
        self.remove()
        self.create()
        return self

    def next(self):
        """Создание объекта со следующим свободным ключом"""
        _sn = self.get_next_serial_number(self._sko)
        self._key = f"{self._sko}_{_sn}"
        self.create()
        return self

    @staticmethod
    def get_next_serial_number(_sko):
        """Получение следующего свободного серийного номера для указанного типа"""
        data = Db.find("Sko", _sko, {}, sort={"_sn": -1}, limit=1)
        if data:
            return data[0]["_sn"] + 1
        return 1