from django.urls import path
from .api import (
    ThrottleTestAPI,
    ThrottleTestAPIRateLimit,
    ThrottleTestAPIRoleBasedRateLimit,
)

urlpatterns = [
    path("", ThrottleTestAPI.as_view()),
    path("rate_limit/", ThrottleTestAPIRateLimit.as_view()),
    path("role_based_rate_limit/", ThrottleTestAPIRoleBasedRateLimit.as_view()),
]
