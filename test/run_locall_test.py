import unittest
import sys

from test.local_test.key_store_model_test import TestKeyStoreModel
from test.local_test.key_store_service_test import TestKeyStoreService

if __name__ == '__main__':
    model = unittest.TestLoader().loadTestsFromTestCase(TestKeyStoreModel)
    service = unittest.TestLoader().loadTestsFromTestCase(TestKeyStoreService)
    all_tests = unittest.TestSuite([model, service])
    result = unittest.TextTestRunner(verbosity=2).run(all_tests)
    if result.wasSuccessful():
        sys.exit(0)
    sys.exit(-1)
