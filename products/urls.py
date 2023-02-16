from django.urls import path
from .apis import *

urlpatterns = [
    path('api/list/', ProductsListAPI.as_view()),
]