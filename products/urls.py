from django.urls import path
from .apis import ProductsListAPI, ProductDynamicAPI, OrderDynamicAPI

urlpatterns = [
    path('api/list/', ProductsListAPI.as_view()),
    path('api/list/dynamic/', ProductDynamicAPI.as_view()),
    path('order/api/list/dynamic/', OrderDynamicAPI.as_view()),
]
