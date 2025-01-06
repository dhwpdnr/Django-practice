from rest_framework.throttling import BaseThrottle
import time
from django.core.cache import cache


class IPBasedThrottle(BaseThrottle):
    def allow_request(self, request, view):
        ip = self.get_client_ip(request)
        cache_key = f"rate_limit_{ip}"
        current_time = time.time()
        last_request_time = cache.get(cache_key)

        # print(f"Cache Key: {cache_key}, Last Request Time: {last_request_time}")
        # print(f"Current Time: {current_time}")
        # print(f"Time Difference: {current_time - (last_request_time or 0)}")

        if last_request_time and current_time - last_request_time < 60:
            return False

        # 요청 허용
        cache.set(cache_key, current_time, timeout=60)
        return True

    def get_client_ip(self, request):
        x_forwarded_for = request.META.get("HTTP_X_FORWARDED_FOR")
        if x_forwarded_for:
            return x_forwarded_for.split(",")[0]
        return request.META.get("REMOTE_ADDR")

    def wait(self):
        return 60
