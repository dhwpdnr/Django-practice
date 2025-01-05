from django.urls import path
from .views import RequestTestAPI

urlpatterns = [path("", RequestTestAPI.as_view())]
