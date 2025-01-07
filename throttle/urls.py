from django.urls import path
from .api import (
    ThrottleTestAPI,
    ThrottleTestAPIRateLimit,
    ThrottleTestAPIRoleBasedRateLimit,
    ThrottleTestAPICustom,
)

urlpatterns = [
    path("", ThrottleTestAPI.as_view()),
    path("rate_limit/", ThrottleTestAPIRateLimit.as_view()),
    path("role_based_rate_limit/", ThrottleTestAPIRoleBasedRateLimit.as_view()),
    path("custom/", ThrottleTestAPICustom.as_view()),
]
