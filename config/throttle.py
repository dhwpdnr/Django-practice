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


class RateLimitThrottle(BaseThrottle):
    rate_limit = 3  # 1분에 허용되는 최대 요청 수
    duration = 5  # 제한 시간 (초)

    def allow_request(self, request, view):
        ip = self.get_client_ip(request)
        cache_key = f"rate_limit_{ip}"
        current_time = time.time()

        # 캐시에서 요청 기록 가져오기
        request_timestamps = cache.get(cache_key, [])

        # 현재 시간 기준으로 유효한 요청만 필터링
        request_timestamps = [
            timestamp
            for timestamp in request_timestamps
            if current_time - timestamp < self.duration
        ]

        if len(request_timestamps) >= self.rate_limit:
            # 요청 제한 초과
            return False

        # 요청 기록 갱신
        request_timestamps.append(current_time)
        cache.set(cache_key, request_timestamps, timeout=self.duration)
        return True

    def get_client_ip(self, request):
        x_forwarded_for = request.META.get("HTTP_X_FORWARDED_FOR")
        if x_forwarded_for:
            return x_forwarded_for.split(",")[0]
        return request.META.get("REMOTE_ADDR")

    def wait(self):
        return self.duration
