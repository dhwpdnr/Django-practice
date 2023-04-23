from django.urls import path
from .apis import ProductsListAPI, ProductDynamicAPI

urlpatterns = [
    path('api/list/', ProductsListAPI.as_view()),
    path('api/list/dynamic/', ProductDynamicAPI.as_view()),
]
