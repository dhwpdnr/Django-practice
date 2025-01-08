from django.urls import path
from .views import SSEAPIView

urlpatterns = [path("", SSEAPIView.as_view())]
