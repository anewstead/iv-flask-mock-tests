import unittest
from src import app


class TestShopEndpoints(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()
        return super().setUp()

    def tearDown(self) -> None:
        return super().tearDown()