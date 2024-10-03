from base import Db, Metadata, Sdo

class Meta:

    @staticmethod
    def init_all():
        print
        Meta.init_sdo()
        Meta.init_sko()
        # Meta.init_sn()

    @staticmethod
    def init_sdo():
        Db.delete_many(Db.Sdo, Db.sdo, {})
        Db.insert(Db.Sdo, Db.sdo, Sdo.upload())

    @staticmethod
    def init_sko():
        Db.delete_many(Db.Meta, Db.sko, {})
        Db.insert(Db.Meta, Db.sko, Metadata.keySyntax)
        Db.insert(Db.Meta, Db.sko, Metadata.skoBody)
        Db.insert(Db.Meta, Db.sko, Metadata.docFrames)
        Db.insert(Db.Meta, Db.sko, Metadata.imageFrames)
        Db.insert(Db.Meta, Db.sko, Metadata.regFrames)

    @staticmethod
    def init_sn():
        Db.delete_many(Db.Meta, Db.sn, {})
        Db.onsert(Db.Meta, Db.sn, Metadata.sn)

    @staticmethod
    def sn(_sko):
        return Db.find_one(Db.Meta, Db.sn, {"_sko": _sko, "_metaType": "serialNumber"}, {"_sn": 1, "_id": 0})["_sn"]

    @staticmethod
    def next_sn(_sko):
        _sn = Meta.sn(_sko)
        Db.update_one(Db.Meta, Db.sn, {"_sko": _sko}, {"$inc": {"_sn": 1}})
        return _sn

    @staticmethod
    def key(_sko):
        return Db.find_one(Db.Meta, Db.sko, {"_sko": _sko, "_metaType": "keySyntax"})["key"]

    @staticmethod
    def keys():
        return Db.find(Db.Meta, Db.sko, {"_metaType": "keySyntax"}, {"_sko": 1, "key": {"syntax": 1}, "_id": 0})

    @staticmethod
    def sko_body(_sko):
        return Db.find_one(Db.Meta, Db.sko, {"_sko": _sko, "_metaType": "skoBody"})["body"]

    @staticmethod
    def image_frame(_sko):
        return Db.find_one(Db.Meta, Db.sko, {"_sko": _sko, "_metaType": "imageFrame"}, {"_drive": 1, "_folder": 1, "_id": 0})

    @staticmethod
    def reg_frame(_sko, _name="ui", _last_version=True, _version=None):
        query = {"_sko": _sko, "_metaType": "regFrame", "_name": _name}
        if _version is None:
            query["_lastVersion"] = _last_version
        else:
            query["_version"] = _version
        return Db.find_one(Db.Meta, Db.sko, query, {"_id": 0})

    @staticmethod
    def doc_frame(_sko, _name="ui", _last_version=True, _version=None):
        query = {"_sko": _sko, "_metaType": "docFrame", "_name": _name}
        if _version is None:
            query["_lastVersion"] = _last_version
        else:
            query["_version"] = _version
        return Db.find_one(Db.Meta, Db.sko, query, {"_id": 0})

# Инициализация метаданных
Meta.init_all()