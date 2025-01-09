from django.urls import path
from .views import TableWithFieldsCreateView

urlpatterns = [
    path("table", TableWithFieldsCreateView.as_view(), name="create-table-with-fields"),
]
