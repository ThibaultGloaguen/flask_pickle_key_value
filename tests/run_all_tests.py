import unittest
import sys

from tests.local_test.key_store_model_test import TestKeyStoreModel
from tests.local_test.key_store_service_test import TestKeyStoreService
from tests.integration_test.route_test import TestRoute

if __name__ == '__main__':

    model = unittest.TestLoader().loadTestsFromTestCase(TestKeyStoreModel)
    service = unittest.TestLoader().loadTestsFromTestCase(TestKeyStoreService)
    integration = unittest.TestLoader().loadTestsFromTestCase(TestRoute)
    all_tests = unittest.TestSuite([model, service, integration])
    result = unittest.TextTestRunner(verbosity=2).run(all_tests)
    if result.wasSuccessful():
        sys.exit(0)
    sys.exit(-1)
