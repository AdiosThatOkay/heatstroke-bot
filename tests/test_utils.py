import hsbot
from hsbot.utils.utils import (
    get_nearest_observatory, postback_data_to_dict
)
from hsbot.scripts.db import InitDB
import os
import tempfile
import unittest


class TestUtils(unittest.TestCase):

    def setUp(self):
        self.db_fd, hsbot.DATABASE = tempfile.mkstemp()
        self.app = hsbot.app.test_client()
        InitDB().run()

    def tearDown(self):
        os.close(self.db_fd)
        os.unlink(hsbot.DATABASE)

    def test_nearest_observatory(self):
        lat0, lon0 = (35.4358333, 139.5191666)
        nearest0 = get_nearest_observatory(lat0, lon0)
        self.assertEqual("46091", nearest0.code)

        lat1, lon1 = (35.4358334, 139.5191667)
        nearest1 = get_nearest_observatory(lat1, lon1)
        self.assertEqual("46106", nearest1.code)

    def test_postback_data_to_dict(self):
        data0 = "change=1&code=46166"
        result0 = postback_data_to_dict(data0)
        self.assertEqual(dict, type(result0))
        self.assertEqual(True, result0['change'])
        self.assertEqual("46166", result0['code'])

        data1 = "change=0"
        result1 = postback_data_to_dict(data1)
        self.assertEqual(dict, type(result1))
        self.assertEqual(False, result1['change'])
