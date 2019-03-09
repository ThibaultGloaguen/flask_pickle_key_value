import fnmatch
import sys

from appplication.models.key_store_model import KeyStoreModel
from appplication.services.database_service import DatabaseService
from dateutil import parser
from datetime import datetime


class KeyStoreService(DatabaseService):
    def __init__(self):
        DatabaseService.__init__(self)

    def get_entity(self, key):
        entity_from_db = self.get(key)

        date_creation, time_to_live, value = self.get_entity_fields(entity_from_db)

        return KeyStoreModel(value, date_creation, time_to_live)

    @staticmethod
    def get_entity_fields(entity_from_db):
        errors = []
        value = entity_from_db.get('value')
        date_creation = entity_from_db.get('date_creation')
        time_to_live = entity_from_db.get('time_to_live')
        if not value:
            errors.append('value')
        if not date_creation:
            errors.append('date_creation')

        if len(errors) > 0:
            raise Exception('Corrupted data: missing %s from entity in DB' % ', '.join(errors))

        date_creation = parser.parse(date_creation)
        if time_to_live:
            time_to_live = int(time_to_live)

        return date_creation, time_to_live, value

    def get_values(self, filter=None):
        all_keys = self.get_all_keys()

        all_keys = self.filter_keys(all_keys, filter)

        entity_list = [self.get_entity(key) for key in all_keys]

        return [entity.value for entity in entity_list if
                not entity.is_expired]

    @staticmethod
    def filter_keys(all_keys, filter):
        if filter:
            all_keys = fnmatch.filter(all_keys, filter.replace('$', '*'))
        return all_keys

    def set_entities(self, json_payload, expire_in):
        keys_not_persisted = []
        if expire_in:
            expire_in = int(expire_in)
        for key, value in json_payload.iteritems():
            success = self.set(str(key), KeyStoreModel(value,
                                                       date_creation=datetime.now(),
                                                       time_to_live=expire_in).to_dict())
            if success:
                sys.stdout.write(" key/value  %s - %s inserted in DB\n" % (key, value))
            else:
                sys.stdout.write(" key/value  %s - %s was not inserted in DB\n" % (key, value))
                keys_not_persisted.append(key)

        return keys_not_persisted
