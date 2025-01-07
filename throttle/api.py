from rest_framework import generics
from rest_framework.response import Response
from config.throttle import (
    IPBasedThrottle,
    RateLimitThrottle,
    RoleBasedRateLimitThrottle,
    CustomThrottle,
)


class ThrottleTestAPI(generics.GenericAPIView):
    throttle_classes = [IPBasedThrottle]

    def get(self, request):
        return Response({"message": "Success!"})


class ThrottleTestAPIRateLimit(generics.GenericAPIView):
    throttle_classes = [RateLimitThrottle]

    def get(self, request):
        return Response({"message": "Success!"})


class ThrottleTestAPIRoleBasedRateLimit(generics.GenericAPIView):
    throttle_classes = [RoleBasedRateLimitThrottle]

    def get(self, request):
        return Response({"message": "Success!"})


class ThrottleTestAPICustom(generics.GenericAPIView):
    throttle_classes = [CustomThrottle]

    def get(self, request):
        return Response({"message": "Success!"})
