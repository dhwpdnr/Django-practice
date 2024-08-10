from django.urls import path
from .views import QueryTestAPI

urlpatterns = [
    path("test", QueryTestAPI.as_view()),
]
