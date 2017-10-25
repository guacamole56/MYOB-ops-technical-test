import json
import os
import unittest

import myob_ops_technical_test
from myob_ops_technical_test.helper import get_last_commit_sha


class MYOBOpsTechTestWebsiteTestEndpoints(unittest.TestCase):
    """ Basic enpoint tests. Check for 200 HTTP response code. """

    def setUp(self):
        myob_ops_technical_test.app.testing = True
        self.app = myob_ops_technical_test.app.test_client()

    def test_root_http_code(self):
        rv = self.app.get('/')
        self.assertEqual(rv.status_code, 200)

    def test_health_http_code(self):
        rv = self.app.get('/health')
        self.assertEqual(rv.status_code, 200)

    def test_metadata_http_code(self):
        rv = self.app.get('/metadata')
        self.assertEqual(rv.status_code, 200)


class MYOBOpsTechTestWebsiteTestContent(unittest.TestCase):
    """ Basic verification of the content served by each endpoint. """

    def setUp(self):
        myob_ops_technical_test.app.testing = True
        self.app = myob_ops_technical_test.app.test_client()

    def test_root_content(self):
        rv = self.app.get('/')
        self.assertIn(b'Hello World!', rv.data)

    def test_health_content(self):
        rv = self.app.get('/health')
        self.assertIn(b'OK', rv.data)

    def test_metadata_content(self):
        rv = self.app.get('/metadata')
        data = json.loads(rv.data)
        print(data)
        self.assertIsNotNone(data['app_name'])
        self.assertIsNotNone(data['description'])
        self.assertIsNotNone(data['last_commit_sha'])
        self.assertIsNotNone(data['version'])


class GetLastCommitSHATest(unittest.TestCase):
    """ Test get_last_commit_sha() function. """

    def setUp(self):
        self.protected_test_version_file = os.path.join(
                os.path.dirname(os.path.realpath(__file__)),
                "files/protected_version.txt"
                )
        os.chmod(self.protected_test_version_file, 0o000)

    def tearDown(self):
        os.chmod(self.protected_test_version_file, 0o600)

    def test_version_with_unreadable_file(self):
        """Expect 'Unknown/Error' if version file exists but is unreadable.
        """

        self.assertEqual(get_last_commit_sha(file_name=self.protected_test_version_file),
                         'Unknown/Error')

    def test_version_no_file(self):
        self.assertEqual(get_last_commit_sha(),
                         'Development')


if __name__ == '__main__':
    unittest.main()
