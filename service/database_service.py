import pickledb
import fnmatch
from model.key_model import KeyModel


class DatabaseService:
    def __init__(self):
        self.db = pickledb.load('key_value_store.db', True)

    def get(self, key):
        return self.db.get(key)

    def exists(self, key):
        return self.db.exists(key)

    def delete(self, id):
        return self.db.drem(id)

    def delete_all(self):
        return self.db.deldb()

    def get_all_values(self, filter=None):
        all_keys = self.db.getall()
        if filter:
            all_keys = fnmatch.filter(all_keys, filter.replace('$', '*'))
        return [self.get(key) for key in all_keys]

    def put(self, json_payload, expire_in=None):
        for key, value in json_payload.iteritems():
            value_object = KeyModel(value, expire_in)
            self.db.set(str(key), value_object.to_dict())
        return json_payload
