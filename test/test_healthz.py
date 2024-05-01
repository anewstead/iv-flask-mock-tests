import unittest
from src.app import app


class TestHealthzEndpoint(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()
        return super().setUp()

    def test_healthz(self):
        response = self.app.get("/healthz")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, b"ok")

    def tearDown(self) -> None:
        return super().tearDown()
