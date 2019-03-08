import unittest
from datetime import datetime
from appplication.services.key_store_service import KeyStoreService


class TestKeyStoreService(unittest.TestCase):

    def test_get_entity_fields_nominal_case(self):
        entity_from_db = {
            'date_creation': '2019-03-06 22:44:32',
            'value': 'my value',
            'time_to_live': '10'
        }
        date_creation, time_to_live, value = KeyStoreService.get_entity_fields(entity_from_db)
        self.assertEqual(date_creation, datetime.strptime('2019-03-06 22:44:32', "%Y-%m-%d %H:%M:%S"))
        self.assertEqual(value, 'my value')
        self.assertEqual(time_to_live, 10)

    def test_get_entity_fields_missing_value(self):
        entity_from_db = {
            'date_creation': '2019-03-06 22:44:32',
            'time_to_live': '10'
        }
        try:
            KeyStoreService.get_entity_fields(entity_from_db)
            self.fail('shall fail')
        except Exception as e:
            self.assertEqual(e.message, 'Corrupted data: missing value from entity in DB')

    def test_get_entity_fields_missing_value_and_date_creation(self):
        entity_from_db = {
            'time_to_live': '10'
        }
        try:
            KeyStoreService.get_entity_fields(entity_from_db)
            self.fail('shall fail')
        except Exception as e:
            self.assertEqual(e.message, 'Corrupted data: missing value, date_creation from entity in DB')

    def test_filter_keys_without_wildcard(self):
        all_keys = ['wod', 'world', 'word', 'test', 'toto']
        filter = 'wod'
        filtered_keys = KeyStoreService.filter_keys(all_keys, filter)
        self.assertEqual(filtered_keys, ['wod'])

    def test_filter_keys_with_wildcard(self):
        all_keys = ['wod', 'world', 'word', 'test', 'toto']
        filter = 'wo$d'
        filtered_keys = KeyStoreService.filter_keys(all_keys, filter)
        self.assertEqual(filtered_keys, ['wod', 'world', 'word'])

    def test_filter_keys_with_empty_filter(self):
        all_keys = ['wod', 'world', 'word', 'test', 'toto']
        filter = None
        filtered_keys = KeyStoreService.filter_keys(all_keys, filter)
        self.assertEqual(filtered_keys, ['wod', 'world', 'word', 'test', 'toto'])

    def test_filter_keys_with_empty_list(self):
        all_keys = []
        filter = 'test'
        filtered_keys = KeyStoreService.filter_keys(all_keys, filter)
        self.assertEqual(filtered_keys, [])
