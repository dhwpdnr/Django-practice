from django.urls import path
from .api import ThrottleTestAPI, ThrottleTestAPIRateLimit

urlpatterns = [path("", ThrottleTestAPI.as_view())]
urlpatterns += [path("rate_limit/", ThrottleTestAPIRateLimit.as_view())]
