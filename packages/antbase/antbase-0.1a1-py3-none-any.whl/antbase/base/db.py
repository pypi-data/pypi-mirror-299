from __future__ import annotations
from pymongo import MongoClient, IndexModel, ASCENDING, DESCENDING
from bson import json_util, ObjectId
import re
from datetime import datetime
from typing import Tuple

from antbase import Auth

class Db:

    __client = Auth.get_db_client()

    # I N D E X E S

    index_sko = [
            IndexModel([("_id" ,ASCENDING)], unique=True),
            IndexModel([("_key",ASCENDING)], unique=True),
            IndexModel([("_sko",ASCENDING)], unique=False)]

    # C O L L E C T I O N S
    Catalog_sko = ("Catalog", "sko")
    Meta_       = ("Meta", "?")
    Qu_lock     = ("Qu", "lock")
    Qu_qu       = ("Qu", "qu")

    Sdo_sdo     = ("sdo", "sdo")

    Sko_cjob    = ("sko", "cjob",    index_sko)
    Sko_order   = ("sko", "order",   index_sko)
    sko_person  = ("sko", "person",  index_sko)
    sko_trigger = ("sko", "trigger", index_sko)

    test_c_1    = ("test","c_1")        # Тестовая база


    def __init__(self, collection: Tuple[str, str]):
        self.collection = Db.__client[collection[0]][collection[1]]
 

    def encode(self, o):
        if isinstance(o, CustomType):
            return o.to_bson()
        if isinstance(o, list):
            return [self.encode(i) for i in o]
        if isinstance(o, dict):
            return {k: self.encode(v) for k, v in o.items()}
        return o

    def decode(self, o):
        if isinstance(o, dict):
            if "$custom_type" in o:
                return CustomType.from_bson(o)
            return {k: self.decode(v) for k, v in o.items()}
        if isinstance(o, list):
            return [self.decode(i) for i in o]
        return o
    
    
    def find_one(self, filter, projection=None):
        result = self.collection.find_one(filter, projection)
        return self.decode(result)
    
    def find(self, filter, projection=None, sort=None, limit=0, skip=0):
        cursor = self.collection.find(filter, projection)
        if sort:
            if isinstance(sort, list) and all(isinstance(i, tuple) and len(i) == 2 for i in sort):
                cursor = cursor.sort(sort)
            else:
                raise TypeError("sort must be a list of tuples with field name and direction")
        cursor = cursor.limit(limit).skip(skip)
        return [self.decode(doc) for doc in cursor]
    
    def insert_one(self, document):
        document = self.encode(document)  # Преобразуем документ перед вставкой
        result = self.collection.insert_one(document)
        return str(result.inserted_id)
    
    def insert(self, documents):
        documents = [self.encode(doc) for doc in documents]  # Преобразуем документы перед вставкой
        result = self.collection.insert_many(documents)
        return [str(id) for id in result.inserted_ids]
    
    def update_one(self, filter, update, upsert=False):
        filter = self.encode(filter)  # Преобразуем фильтр перед обновлением
        update = self.encode(update)  # Преобразуем обновление перед обновлением
        result = self.collection.update_one(filter, update, upsert=upsert)
        return {"matchedCount": result.matched_count, "modifiedCount": result.modified_count}
    
    def update(self, filter, update, upsert=False):
        filter = self.encode(filter)  # Преобразуем фильтр перед обновлением
        update = self.encode(update)  # Преобразуем обновление перед обновлением
        result = self.collection.update_many(filter, update, upsert=upsert)
        return {"matchedCount": result.matched_count, "modifiedCount": result.modified_count}
    
    def delete_one(self, filter):
        filter = self.encode(filter)  # Преобразуем фильтр перед удалением
        result = self.collection.delete_one(filter)
        return result.deleted_count
    
    def delete_many(self, filter):
        filter = self.encode(filter)  # Преобразуем фильтр перед удалением
        result = self.collection.delete_many(filter)
        return result.deleted_count
    
    def aggregate(self, pipeline):
        pipeline = [self.encode(stage) for stage in pipeline]  # Преобразуем pipeline перед агрегацией
        cursor = self.collection.aggregate(pipeline)
        return [self.decode(doc) for doc in cursor]
    
    def create_index(self, keys, **kwargs):
        keys = self.encode(keys)  # Преобразуем ключи перед созданием индекса
        result = self.collection.create_index(keys, **kwargs)
        return result
    
    def create_indexes(self, indexes):
        indexes = [self.encode(index) for index in indexes]  # Преобразуем индексы перед созданием
        result = self.collection.create_indexes(indexes)
        return result
    

class CustomType:
    def __init__(self, value):
        self.value = value

    def to_bson(self):
        return {"custom_type": self.value}

    @staticmethod
    def from_bson(bson_data):
        return CustomType(bson_data["custom_type"])