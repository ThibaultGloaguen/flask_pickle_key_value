from appplication import db


class DatabaseService:
    def __init__(self):
        self.db = db

    def get(self, key):
        return self.db.get(key)

    def exists(self, key):
        return self.db.exists(key)

    def delete(self, key):
        return self.db.drem(key)

    def delete_all(self):
        return self.db.deldb()

    def get_all_keys(self):
        return self.db.getall()

    def set(self, key, value):
        return self.db.set(key, value)
