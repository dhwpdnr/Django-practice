from django.urls import path
from .api import ThrottleTestAPI

urlpatterns = [path("", ThrottleTestAPI.as_view())]
