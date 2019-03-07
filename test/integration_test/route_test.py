import unittest
import time
from appplication import app


class TestRoute(unittest.TestCase):
    app.config['DATABASE'] = 'key_value_store_for_test_only.db'
    client = app.test_client()

    def test_get_all_values_empty_db(self):
        rv = self.client.get('/keys')
        self.assertEqual(rv.get_json(), {"response": []})
        self.assertEqual(rv.status_code, 200)

    def test_add_get_delete_key(self):
        rv = self.client.put('/keys', json={'my_key': 'my_value'})
        self.assertEqual(rv.status_code, 200)
        self.assertEqual(rv.get_json(), {'response': 'all key value pair are persisted'})

        rv = self.client.get('/keys/my_key')
        self.assertEqual(rv.get_json(), {"response": 'my_value'})
        self.assertEqual(rv.status_code, 200)

        rv = self.client.delete('/keys/my_key')
        self.assertEqual(rv.get_json(), {"response": 'my_key has been deleted'})
        self.assertEqual(rv.status_code, 200)

    def test_add_get_multiple_key(self):
        rv = self.client.put('/keys', json={'my_key': 'my_value', 'my_key_2': 'my_value_2'})
        self.assertEqual(rv.status_code, 200)
        self.assertEqual(rv.get_json(), {'response': 'all key value pair are persisted'})

        rv = self.client.get('/keys/my_key')
        self.assertEqual(rv.get_json(), {"response": 'my_value'})
        self.assertEqual(rv.status_code, 200)

        rv = self.client.get('/keys/my_key_2')
        self.assertEqual(rv.get_json(), {"response": 'my_value_2'})
        self.assertEqual(rv.status_code, 200)

        rv = self.client.get('/keys')
        self.assertEqual(rv.get_json(), {"response": ['my_value_2', 'my_value']})
        self.assertEqual(rv.status_code, 200)

        self.clean_db()

    def test_get_multiple_key_filtered(self):
        rv = self.client.put('/keys', json={'my_key': 'my_value', 'mykey': 'my_value_2'})
        self.assertEqual(rv.status_code, 200)
        self.assertEqual(rv.get_json(), {'response': 'all key value pair are persisted'})

        rv = self.client.get('/keys?filter=my$key')
        self.assertEqual(rv.get_json(), {"response": ['my_value', 'my_value_2']})
        self.assertEqual(rv.status_code, 200)

        self.clean_db()

    def test_add_key_with_ttl(self):
        rv = self.client.put('/keys?expire_in=5', json={'my_key': 'my_value'})
        self.assertEqual(rv.status_code, 200)
        self.assertEqual(rv.get_json(), {'response': 'all key value pair are persisted'})

        rv = self.client.get('/keys/my_key')
        self.assertEqual(rv.get_json(), {"response": 'my_value'})
        self.assertEqual(rv.status_code, 200)
        time.sleep(6)

        rv = self.client.get('/keys/my_key')
        self.assertEqual(rv.get_json(), {"error": 'Expired'})
        self.assertEqual(rv.status_code, 410)

        rv = self.client.delete('/keys')
        self.assertEqual(rv.status_code, 200)

    def test_get_key_not_found(self):
        rv = self.client.get('/keys/key_not_found')
        self.assertEqual(rv.status_code, 404)
        self.assertEqual(rv.get_json(), {'error': 'Not found'})

    def clean_db(self):
        rv = self.client.delete('/keys')
        self.assertEqual(rv.status_code, 200)
