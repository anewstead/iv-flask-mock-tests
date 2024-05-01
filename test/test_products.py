import unittest
from src.app import app


class TestProductsEndpoints(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()
        return super().setUp()

    def tearDown(self) -> None:
        return super().tearDown()
