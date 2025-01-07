from rest_framework.throttling import BaseThrottle
from django.core.cache import cache
import time
from rest_framework.exceptions import Throttled


class CustomThrottle(BaseThrottle):
    default_rate_limit = 5  # 기본 요청 수
    default_duration = 10  # 제한 시간 (초)

    def allow_request(self, request, view):
        ip = self.get_client_ip(request)
        cache_key = f"rate_limit_{ip}"
        current_time = time.time()

        # 요청 기록 가져오기
        request_timestamps = cache.get(cache_key, [])

        # 유효한 요청만 필터링
        request_timestamps = [
            timestamp
            for timestamp in request_timestamps
            if current_time - timestamp < self.default_duration
        ]

        if len(request_timestamps) >= self.default_rate_limit:
            self.throttle_timeout = self.default_duration - (
                current_time - request_timestamps[-1]
            )
            self.raise_throttled_error(request)
            return False

        # 요청 기록 갱신
        request_timestamps.append(current_time)
        cache.set(cache_key, request_timestamps, timeout=self.default_duration)
        return True

    def raise_throttled_error(self, request):
        """
        요청 제한 초과 시 커스텀 Throttled 예외를 발생시킵니다.
        """
        detail = {
            "error": "Too many requests",
            "message": f"요청량 한도를 초과했습니다. {self.throttle_timeout:.1f}초 후에 다시 시도하세요.",
        }
        raise Throttled(detail=detail)

    def get_client_ip(self, request):
        """
        클라이언트의 IP 주소를 가져옵니다.
        """
        x_forwarded_for = request.META.get("HTTP_X_FORWARDED_FOR")
        if x_forwarded_for:
            return x_forwarded_for.split(",")[0]
        return request.META.get("REMOTE_ADDR")


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

        # 요청 제한 초과
        if len(request_timestamps) >= self.rate_limit:
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


class RoleBasedRateLimitThrottle(BaseThrottle):
    default_rate_limit = 10
    default_duration = 60

    # 권한 그룹별 제한 설정
    rate_limits = {
        "admin": (100, 60),  # 관리자: 1분에 100개의 요청
        "premium": (50, 60),  # 프리미엄 사용자: 1분에 50개의 요청
        "basic": (10, 60),  # 기본 사용자: 1분에 10개의 요청
    }

    # rate_limits = {
    #     'admin': {"rate_limit": 100, "duration": 60},  # 관리자: 1분에 100개의 요청
    #     'premium': {"rate_limit": 50, "duration": 60},  # 프리미엄 사용자: 1분에 50개의 요청
    #     'basic': {"rate_limit": 10, "duration": 60},  # 기본 사용자: 1분에 10개의 요청
    # }

    def allow_request(self, request, view):
        # 사용자 그룹에 따른 제한 값 가져오기
        role = self.get_user_role(request)
        rate_limit, duration = self.rate_limits.get(
            role, (self.default_rate_limit, self.default_duration)
        )

        ip = self.get_client_ip(request)
        role = self.get_user_role(request)
        cache_key = f"rate_limit_{role}_{ip}"
        current_time = time.time()

        # 캐시에서 요청 기록 가져오기
        request_timestamps = cache.get(cache_key, [])

        # 현재 시간 기준으로 유효한 요청만 필터링
        request_timestamps = [
            timestamp
            for timestamp in request_timestamps
            if current_time - timestamp < duration
        ]

        if len(request_timestamps) >= rate_limit:
            # 요청 제한 초과
            return False

        # 요청 기록 갱신
        request_timestamps.append(current_time)
        cache.set(cache_key, request_timestamps, timeout=duration)
        return True

    def get_user_role(self, request):
        if request.user.is_superuser:
            return "admin"
        elif request.user.group == "premium":
            return "premium"
        else:
            return "basic"

    def get_client_ip(self, request):
        x_forwarded_for = request.META.get("HTTP_X_FORWARDED_FOR")
        if x_forwarded_for:
            return x_forwarded_for.split(",")[0]
        return request.META.get("REMOTE_ADDR")

    def wait(self):
        return self.default_duration


class CustomThrottle(BaseThrottle):
    default_rate_limit = 5  # 기본 요청 수
    default_duration = 10  # 제한 시간 (초)

    def allow_request(self, request, view):
        ip = self.get_client_ip(request)
        cache_key = f"rate_limit_{ip}"
        current_time = time.time()

        # 요청 기록 가져오기
        request_timestamps = cache.get(cache_key, [])

        # 유효한 요청만 필터링
        request_timestamps = [
            timestamp
            for timestamp in request_timestamps
            if current_time - timestamp < self.default_duration
        ]

        if len(request_timestamps) >= self.default_rate_limit:
            self.throttle_timeout = self.default_duration - (
                current_time - request_timestamps[-1]
            )
            self.raise_throttled_error(request)
            return False

        # 요청 기록 갱신
        request_timestamps.append(current_time)
        cache.set(cache_key, request_timestamps, timeout=self.default_duration)
        return True

    def raise_throttled_error(self, request):
        """
        요청 제한 초과 시 커스텀 Throttled 예외를 발생
        """
        detail = {
            "error": "Too many requests",
            "message": f"요청량 한도를 초과했습니다. {self.throttle_timeout:.1f}초 후에 다시 시도하세요.",
        }
        raise Throttled(detail=detail)

    def get_client_ip(self, request):
        """
        클라이언트의 IP 주소를 가져옴
        """
        x_forwarded_for = request.META.get("HTTP_X_FORWARDED_FOR")
        if x_forwarded_for:
            return x_forwarded_for.split(",")[0]
        return request.META.get("REMOTE_ADDR")
