from django.urls import path
from .views import TableWithFieldsCreateView, DynamicTableDataCreateView

urlpatterns = [
    path("table", TableWithFieldsCreateView.as_view(), name="create-table-with-fields"),
    path(
        "table/<int:table_id>/data",
        DynamicTableDataCreateView.as_view(),
        name="create-dynamic-data",
    ),
]
