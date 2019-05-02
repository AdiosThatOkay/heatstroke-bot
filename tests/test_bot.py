import os
import hsbot
import unittest
import tempfile
from hsbot.scripts.db import InitDB


class TestBot(unittest.TestCase):

    def setUp(self):
        self.db_fd, hsbot.DATABASE = tempfile.mkstemp()
        self.app = hsbot.app.test_client()
        InitDB().run()

    def tearDown(self):
        os.close(self.db_fd)
        os.unlink(hsbot.DATABASE)

    def test_connect(self):
        res = self.app.get('/')
        self.assertEqual(200, res.status_code)
        self.assertIn('This is Test.'.encode(), res.data)
