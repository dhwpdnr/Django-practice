from django.urls import path
from .views import log_monitoring_page, read_logs

urlpatterns = [
    path("monitor", log_monitoring_page),
    path("read-json", read_logs),
]
