from django.test import TestCase
from django.core.cache import cache


class ThrottleAPITest(TestCase):
    def setUp(self):
        cache.clear()

    def test_throttle_api(self):
        response = self.client.get("/throttle/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {"message": "Success!"})

    def test_throttle_api_rate_limit(self):
        response = self.client.get("/throttle/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {"message": "Success!"})

        response = self.client.get("/throttle/")
        self.assertEqual(response.status_code, 429)
        self.assertEqual(
            response.json(),
            {"detail": "Request was throttled. Expected available in 60 seconds."},
        )
