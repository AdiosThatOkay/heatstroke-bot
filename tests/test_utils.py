import hsbot
from hsbot.utils.utils import (
    get_nearest_observatory, get_observatory_name
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

    def test_get_observatory_name(self):
        self.assertEqual("横浜", get_observatory_name("46106"))
