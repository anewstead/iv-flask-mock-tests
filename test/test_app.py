import unittest
from src import app

class HealthzEndpointTest(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()
    
    def test_healthz(self):
        response = self.app.get('/healthz')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, b'ok')
    