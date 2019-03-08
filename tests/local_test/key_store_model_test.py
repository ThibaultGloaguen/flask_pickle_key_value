import unittest
from datetime import datetime
import time
from appplication.models.key_store_model import KeyStoreModel


class TestKeyStoreModel(unittest.TestCase):
    def test_create_key_store_model_without_ttl(self):
        value = 'my value'
        date_creation = datetime.now()
        key_obj = KeyStoreModel(value, date_creation=date_creation)
        self.assertEqual(key_obj.date_creation, date_creation)
        self.assertEqual(key_obj.value, 'my value')
        self.assertIsNone(key_obj.time_to_live)

    def test_create_key_store_model_with_ttl(self):
        value = 'my value'
        date_creation = datetime.now()
        key_obj = KeyStoreModel(value, date_creation=date_creation, time_to_live=10)
        self.assertEqual(key_obj.date_creation, date_creation)
        self.assertEqual(key_obj.value, 'my value')
        self.assertEqual(key_obj.time_to_live, 10)

    def test_create_key_store_model_expire_after_ttl(self):
        value = 'my value'
        date_creation = datetime.now()
        key_obj = KeyStoreModel(value, date_creation=date_creation, time_to_live=4)
        self.assertEqual(key_obj.is_expired, False)
        time.sleep(2)
        self.assertEqual(key_obj.is_expired, False)
        time.sleep(3)
        self.assertEqual(key_obj.is_expired, True)
