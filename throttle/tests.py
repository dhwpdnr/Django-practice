import time
from django.test import TestCase
from django.core.cache import cache
from django.contrib.auth import get_user_model

User = get_user_model()


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

    def test_throttle_rate_limit(self):
        response = self.client.get("/throttle/rate_limit/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {"message": "Success!"})

        response = self.client.get("/throttle/rate_limit/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {"message": "Success!"})

        response = self.client.get("/throttle/rate_limit/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {"message": "Success!"})

        response = self.client.get("/throttle/rate_limit/")
        self.assertEqual(response.status_code, 429)
        self.assertEqual(
            response.json(),
            {"detail": "Request was throttled. Expected available in 5 seconds."},
        )

    def test_throttle_rate_limit_over_duration(self):
        response = self.client.get("/throttle/rate_limit/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {"message": "Success!"})

        response = self.client.get("/throttle/rate_limit/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {"message": "Success!"})

        response = self.client.get("/throttle/rate_limit/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {"message": "Success!"})

        response = self.client.get("/throttle/rate_limit/")
        self.assertEqual(response.status_code, 429)
        self.assertEqual(
            response.json(),
            {"detail": "Request was throttled. Expected available in 5 seconds."},
        )

        # 5초 이후
        time.sleep(5)

        response = self.client.get("/throttle/rate_limit/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {"message": "Success!"})

    def test_role_based_throttle_admin(self):
        admin_user = User.objects.create_superuser(
            first_name="Admin",
            last_name="User",
            email="admin_user@test.com",
            password="admin1234",
            group="admin",
        )
        self.client.force_login(admin_user)

        for _ in range(100):
            response = self.client.get("/throttle/role_based_rate_limit/")
            self.assertEqual(response.status_code, 200)
            self.assertEqual(response.json(), {"message": "Success!"})

        response = self.client.get("/throttle/role_based_rate_limit/")
        self.assertEqual(response.status_code, 429)
        self.assertEqual(
            response.json(),
            {"detail": "Request was throttled. Expected available in 60 seconds."},
        )

        time.sleep(60)

        response = self.client.get("/throttle/role_based_rate_limit/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {"message": "Success!"})

    def test_throttle_response_msg_custom(self):
        for _ in range(5):
            response = self.client.get("/throttle/custom/")
            self.assertEqual(response.status_code, 200)
            self.assertEqual(response.json(), {"message": "Success!"})

        response = self.client.get("/throttle/custom/")
        self.assertEqual(response.status_code, 429)
        self.assertEqual(response.json()["error"], "Too many requests")
        self.assertEqual(
            response.json()["message"], "요청량 한도를 초과했습니다. 10.0초 후에 다시 시도하세요."
        )
