import time
from django.core.cache import cache
from django.http import JsonResponse


class RateLimitMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # 사용자의 IP 주소 가져오기
        ip = self.get_client_ip(request)
        cache_key = f"rate_limit_{ip}"

        # 캐시에서 마지막 요청 시간 가져오기
        last_request_time = cache.get(cache_key)
        current_time = time.time()

        # 요청 제한 여부 확인
        if last_request_time and current_time - last_request_time < 60:
            return JsonResponse(
                {"error": "Too many requests. Please wait 1 minute."}, status=429
            )

        # 요청 허용: 새로운 타임스탬프 저장
        cache.set(cache_key, current_time, timeout=60)
        return self.get_response(request)

    def get_client_ip(self, request):
        """헤더에서 클라이언트 IP 가져오기"""
        x_forwarded_for = request.META.get("HTTP_X_FORWARDED_FOR")
        if x_forwarded_for:
            return x_forwarded_for.split(",")[0]
        return request.META.get("REMOTE_ADDR")
