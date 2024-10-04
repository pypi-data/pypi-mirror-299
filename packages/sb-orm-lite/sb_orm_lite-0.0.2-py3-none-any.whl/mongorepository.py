from typing import TypeVar, Generic, List

from pymongo import MongoClient
from sb_serializer import HardSerializer

T = TypeVar("T")


class MongoRepository(Generic[T]):

    def __init__(self, connection_string: str, database: str, collection: str):
        self.connection_string = connection_string
        self.database = database
        self.collection = collection
        self.client = MongoClient(self.connection_string, uuidRepresentation='standard')
        self.db = self.client[self.database]
        self.collection = self.db[self.collection]
        self.serializer = HardSerializer()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.close()

    def close(self):
        self.client.close()

    def get_one(self, where) -> T:
        data = self.collection.find_one(where)
        if data is not None:
            cls = self.__orig_class__.__args__[0]
            obj: T = self.serializer.map_to_object(data, cls)
            return obj
        return None

    def get_many(self, where) -> List[T]:
        cursor = self.collection.find(where)
        result: List[T] = []
        for data in cursor:
            cls = self.__orig_class__.__args__[0]
            obj: T = self.serializer.map_to_object(data, cls)
            result.append(obj)
        return result

    def add(self, obj: T):
        data = self.serializer.map_to_dict(obj)
        self.collection.insert_one(data)

    def upsert(self, obj: T):
        data = self.serializer.map_to_dict(obj)
        self.collection.replace_one({"_id": obj._id}, data, upsert=True)

    def delete(self, obj: T):
        self.collection.delete_one({"_id": obj._id})
